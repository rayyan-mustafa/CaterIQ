"""Payment processing, Stripe test mode simulation, and idempotent webhook handling."""

from datetime import datetime, timedelta, timezone
import uuid
from typing import Any, Dict
from sqlalchemy.orm import Session
from backend.app.models.billing import Invoice, Payment, Proposal
from backend.app.models.event import Event


def approve_proposal_and_create_deposit_invoice(db: Session, proposal: Proposal) -> Invoice:
    """Approve a proposal and generate its deposit invoice."""
    proposal.status = "approved"
    proposal.approved_at = datetime.now(timezone.utc)

    event = proposal.event
    deposit_amount = round(proposal.total_amount * (proposal.deposit_percent / 100.0), 2)

    # Check if a deposit invoice already exists
    existing = (
        db.query(Invoice)
        .filter(Invoice.event_id == event.id, Invoice.kind == "deposit")
        .first()
    )
    if existing:
        return existing

    invoice = Invoice(
        event_id=event.id,
        organization_id=proposal.organization_id,
        kind="deposit",
        amount=deposit_amount,
        due_date=event.event_date - timedelta(days=14),
        status="unpaid",
    )
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice


def process_payment_confirmation(
    db: Session,
    invoice_id: str,
    raw_event_id: str,
    stripe_payment_intent_id: str = "pi_test_simulated",
) -> Dict[str, Any]:
    """Idempotently process an invoice payment (simulated or via Stripe webhook).

    Guarantees:
    - Same raw_event_id processed twice is ignored (idempotent).
    - Invoice marked as paid.
    - Event confirmed automatically.
    - Automatic creation of the remaining balance invoice.
    """
    # 1. Idempotency check on raw_event_id
    existing_payment = (
        db.query(Payment)
        .filter(Payment.raw_event_id == raw_event_id)
        .first()
    )
    if existing_payment:
        return {
            "status": "already_processed",
            "payment_id": existing_payment.id,
            "invoice_id": existing_payment.invoice_id,
        }

    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise ValueError(f"Invoice {invoice_id} not found.")

    invoice.status = "paid"

    # 2. Record payment row
    payment = Payment(
        invoice_id=invoice.id,
        organization_id=invoice.organization_id,
        stripe_payment_intent_id=stripe_payment_intent_id,
        amount=invoice.amount,
        currency="usd",
        status="succeeded",
        raw_event_id=raw_event_id,
        paid_at=datetime.now(timezone.utc),
    )
    db.add(payment)

    # 3. Update Event status to confirmed
    event = db.query(Event).filter(Event.id == invoice.event_id).first()
    if event and event.status in ("lead", "proposed"):
        event.status = "confirmed"

    # 4. If deposit was paid, auto-create balance invoice due 7 days prior to event
    if invoice.kind == "deposit" and event:
        existing_balance = (
            db.query(Invoice)
            .filter(Invoice.event_id == event.id, Invoice.kind == "balance")
            .first()
        )
        if not existing_balance:
            # Look up proposal total
            prop = (
                db.query(Proposal)
                .filter(Proposal.event_id == event.id)
                .order_by(Proposal.version.desc())
                .first()
            )
            total_amt = prop.total_amount if prop else invoice.amount * 2.0
            balance_amt = round(max(0.0, total_amt - invoice.amount), 2)
            balance_inv = Invoice(
                event_id=event.id,
                organization_id=event.organization_id,
                kind="balance",
                amount=balance_amt,
                due_date=event.event_date - timedelta(days=7),
                status="unpaid",
            )
            db.add(balance_inv)

    db.commit()
    db.refresh(payment)

    return {
        "status": "succeeded",
        "payment_id": payment.id,
        "amount": payment.amount,
        "event_status": event.status if event else None,
    }
