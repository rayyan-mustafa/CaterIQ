"""Proposals and public client review router."""

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from backend.app.core.config import settings
from backend.app.core.database import get_db
from backend.app.core.dependencies import AuthenticatedContext, get_current_context, require_role
from backend.app.models.billing import Invoice, Proposal
from backend.app.models.event import Event
from backend.app.schemas.billing import ProposalCreate, ProposalResponse
from backend.app.services.payment_service import approve_proposal_and_create_deposit_invoice
from backend.app.services.proposal_service import (
    create_event_proposal,
    generate_proposal_html,
)

router = APIRouter(tags=["Proposals & Contracts"])


@router.post("/events/{event_id}/proposals", response_model=ProposalResponse)
def generate_proposal(
    event_id: str,
    req: ProposalCreate,
    ctx: AuthenticatedContext = Depends(require_role(["owner", "manager"])),
    db: Session = Depends(get_db),
):
    """Generate a new versioned proposal for an event."""
    ev = (
        db.query(Event)
        .filter(Event.id == event_id, Event.organization_id == ctx.organization_id)
        .first()
    )
    if not ev:
        raise HTTPException(status_code=404, detail="Event not found.")

    prop = create_event_proposal(db, ev, deposit_percent=req.deposit_percent)
    deposit_amt = round(prop.total_amount * (prop.deposit_percent / 100.0), 2)

    return ProposalResponse(
        id=prop.id,
        event_id=prop.event_id,
        event_title=ev.title,
        client_name=ev.client.name if ev.client else None,
        version=prop.version,
        total_amount=prop.total_amount,
        deposit_percent=prop.deposit_percent,
        deposit_amount=deposit_amt,
        public_token=prop.public_token,
        public_url=f"/p/{prop.public_token}",
        status=prop.status,
        created_at=prop.created_at,
        sent_at=prop.sent_at,
        approved_at=prop.approved_at,
    )


@router.get("/proposals/{proposal_id}/pdf")
def view_proposal_document(
    proposal_id: str,
    ctx: AuthenticatedContext = Depends(get_current_context),
    db: Session = Depends(get_db),
):
    """View printable HTML representation of the proposal."""
    prop = (
        db.query(Proposal)
        .filter(Proposal.id == proposal_id, Proposal.organization_id == ctx.organization_id)
        .first()
    )
    if not prop:
        raise HTTPException(status_code=404, detail="Proposal not found.")

    html_content = generate_proposal_html(prop)
    return Response(content=html_content, media_type="text/html")


# --- PUBLIC CLIENT ENDPOINTS (No Auth Needed) ---
@router.get("/p/{token}")
def get_public_proposal(token: str, db: Session = Depends(get_db)):
    """Public read-only proposal endpoint for clients to review details."""
    prop = db.query(Proposal).filter(Proposal.public_token == token).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Proposal not found or link has expired.")

    ev = prop.event
    deposit_amt = round(prop.total_amount * (prop.deposit_percent / 100.0), 2)

    menu_summary = []
    for it in ev.items:
        menu_summary.append({
            "name": it.menu_item.name,
            "category": it.menu_item.category,
            "quantity": it.quantity,
            "unit_price": it.unit_price,
            "line_total": round(it.unit_price * it.quantity * ev.headcount, 2),
        })

    return {
        "proposal_id": prop.id,
        "token": prop.public_token,
        "status": prop.status,
        "event_title": ev.title,
        "event_date": str(ev.event_date),
        "headcount": ev.headcount,
        "venue": ev.venue_address,
        "total_amount": prop.total_amount,
        "deposit_percent": prop.deposit_percent,
        "deposit_amount": deposit_amt,
        "items": menu_summary,
        "approved_at": prop.approved_at,
    }


@router.post("/p/{token}/approve")
def approve_public_proposal(token: str, db: Session = Depends(get_db)):
    """Client clicks 'Approve & Pay Deposit' -> marks proposal approved and creates deposit invoice."""
    prop = db.query(Proposal).filter(Proposal.public_token == token).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Proposal not found.")

    invoice = approve_proposal_and_create_deposit_invoice(db, prop)

    return {
        "message": "Proposal approved successfully.",
        "status": "approved",
        "invoice_id": invoice.id,
        "deposit_amount": invoice.amount,
        "checkout_url": f"/api/v1/invoices/{invoice.id}/checkout",
    }
