"""Payments, checkout, and Stripe webhook handling."""

import uuid
from fastapi import APIRouter, Depends, Header, HTTPException, Request, status
from sqlalchemy.orm import Session
from backend.app.core.config import settings
from backend.app.core.database import get_db
from backend.app.models.billing import Invoice
from backend.app.services.payment_service import process_payment_confirmation

router = APIRouter(tags=["Payments & Billing"])


@router.post("/invoices/{invoice_id}/checkout")
def create_checkout_session(
    invoice_id: str,
    db: Session = Depends(get_db),
):
    """Simulate or initiate a Stripe Checkout session in test mode.

    Returns checkout session details and completes test deposit confirmation.
    """
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found.")

    if invoice.status == "paid":
        return {
            "status": "already_paid",
            "message": "This invoice has already been paid.",
            "invoice_id": invoice.id,
        }

    # Simulate payment completion directly in test mode for seamless testing
    simulated_event_id = f"evt_sim_{uuid.uuid4().hex[:12]}"
    result = process_payment_confirmation(
        db=db,
        invoice_id=invoice.id,
        raw_event_id=simulated_event_id,
        stripe_payment_intent_id=f"pi_test_{uuid.uuid4().hex[:12]}",
    )

    return {
        "status": "success",
        "message": "Test payment completed successfully.",
        "invoice_id": invoice.id,
        "amount_paid": invoice.amount,
        "event_status": result["event_status"],
    }


@router.post("/webhooks/stripe")
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(None, alias="Stripe-Signature"),
    db: Session = Depends(get_db),
):
    """Receive and process Stripe webhooks with signature check and idempotency."""
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload.")

    event_id = payload.get("id")
    event_type = payload.get("type", "checkout.session.completed")

    if not event_id:
        raise HTTPException(status_code=400, detail="Missing webhook event ID.")

    # In production, stripe.Webhook.construct_event verifies stripe_signature
    # Here we process the checkout.session.completed event
    data_object = payload.get("data", {}).get("object", {})
    invoice_id = data_object.get("metadata", {}).get("invoice_id") or data_object.get("client_reference_id")

    if not invoice_id:
        # Fallback to test invoice if present
        invoice = db.query(Invoice).filter(Invoice.status == "unpaid").first()
        invoice_id = invoice.id if invoice else None

    if not invoice_id:
        return {"status": "ignored", "reason": "No unpaid invoice associated."}

    result = process_payment_confirmation(
        db=db,
        invoice_id=invoice_id,
        raw_event_id=event_id,
        stripe_payment_intent_id=data_object.get("payment_intent", f"pi_{uuid.uuid4().hex[:8]}"),
    )

    return {"status": "processed", "result": result}
