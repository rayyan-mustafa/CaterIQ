"""Proposal generation, versioning, and document formatting services."""

from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.orm import Session
from backend.app.core.config import settings
from backend.app.models.billing import Invoice, Proposal
from backend.app.models.event import Event
from backend.app.services.pricing_service import calculate_event_totals


def create_event_proposal(
    db: Session,
    event: Event,
    deposit_percent: float = 30.0,
) -> Proposal:
    """Create a new versioned proposal for an event."""
    total_rev, _, _, _ = calculate_event_totals(event)

    # Determine next version
    existing_proposals = (
        db.query(Proposal)
        .filter(Proposal.event_id == event.id)
        .order_by(Proposal.version.desc())
        .all()
    )
    next_version = (existing_proposals[0].version + 1) if existing_proposals else 1

    proposal = Proposal(
        event_id=event.id,
        organization_id=event.organization_id,
        version=next_version,
        total_amount=total_rev,
        deposit_percent=deposit_percent,
        status="sent",
        sent_at=datetime.now(timezone.utc),
    )
    db.add(proposal)
    db.commit()
    db.refresh(proposal)
    return proposal


def generate_proposal_html(proposal: Proposal) -> str:
    """Generate professional printable HTML document for client proposals."""
    event = proposal.event
    client = event.client
    deposit_amount = round(proposal.total_amount * (proposal.deposit_percent / 100.0), 2)
    balance_amount = round(proposal.total_amount - deposit_amount, 2)

    items_html = ""
    for item in event.items:
        line_total = round(item.unit_price * item.quantity * event.headcount, 2)
        items_html += f"""
        <tr>
            <td style="padding: 12px; border-bottom: 1px solid #e2e8f0;">{item.menu_item.name}</td>
            <td style="padding: 12px; border-bottom: 1px solid #e2e8f0; text-transform: capitalize;">{item.menu_item.category}</td>
            <td style="padding: 12px; border-bottom: 1px solid #e2e8f0; text-align: center;">{item.quantity} × {event.headcount}</td>
            <td style="padding: 12px; border-bottom: 1px solid #e2e8f0; text-align: right;">${item.unit_price:.2f}</td>
            <td style="padding: 12px; border-bottom: 1px solid #e2e8f0; text-align: right; font-weight: bold;">${line_total:.2f}</td>
        </tr>
        """

    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Proposal #{proposal.version} — {event.title}</title>
    <style>
        body {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; color: #1e293b; margin: 0; padding: 40px; background: #fff; }}
        .header {{ display: flex; justify-content: space-between; border-bottom: 2px solid #0f172a; padding-bottom: 24px; margin-bottom: 32px; }}
        .badge {{ background: #e0e7ff; color: #3730a3; padding: 4px 12px; border-radius: 9999px; font-size: 13px; font-weight: 600; }}
        table {{ width: 100%; border-collapse: collapse; margin: 24px 0; }}
        th {{ background: #f8fafc; padding: 12px; text-align: left; font-size: 13px; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; }}
        .summary-box {{ float: right; width: 340px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; }}
        .summary-row {{ display: flex; justify-content: space-between; padding: 8px 0; }}
        .total-row {{ font-size: 18px; font-weight: bold; border-top: 2px solid #cbd5e1; margin-top: 8px; padding-top: 12px; }}
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1 style="margin: 0 0 8px 0; color: #0f172a;">CaterIQ Event Proposal</h1>
            <p style="margin: 0; color: #64748b;">Proposal Version {proposal.version} &bull; Generated: {proposal.created_at.strftime('%B %d, %Y')}</p>
        </div>
        <div style="text-align: right;">
            <span class="badge">STATUS: {proposal.status.upper()}</span>
        </div>
    </div>

    <div style="display: flex; gap: 40px; margin-bottom: 32px;">
        <div style="flex: 1;">
            <h3 style="margin: 0 0 8px 0; color: #475569; font-size: 14px; text-transform: uppercase;">Client Details</h3>
            <p style="margin: 0 0 4px 0; font-weight: bold; font-size: 16px;">{client.name}</p>
            <p style="margin: 0 0 4px 0; color: #64748b;">{client.company_name or ''}</p>
            <p style="margin: 0; color: #64748b;">{client.email}</p>
        </div>
        <div style="flex: 1;">
            <h3 style="margin: 0 0 8px 0; color: #475569; font-size: 14px; text-transform: uppercase;">Event Information</h3>
            <p style="margin: 0 0 4px 0; font-weight: bold;">{event.title}</p>
            <p style="margin: 0 0 4px 0; color: #64748b;">Date: {event.event_date} ({event.start_time or ''} - {event.end_time or ''})</p>
            <p style="margin: 0; color: #64748b;">Headcount: {event.headcount} Guests &bull; Venue: {event.venue_address or 'On-site'}</p>
        </div>
    </div>

    <table>
        <thead>
            <tr>
                <th>Menu Item</th>
                <th>Category</th>
                <th style="text-align: center;">Headcount</th>
                <th style="text-align: right;">Price / Head</th>
                <th style="text-align: right;">Total</th>
            </tr>
        </thead>
        <tbody>
            {items_html}
        </tbody>
    </table>

    <div class="summary-box">
        <div class="summary-row">
            <span>Subtotal:</span>
            <span>${proposal.total_amount:.2f}</span>
        </div>
        <div class="summary-row" style="color: #4338ca; font-weight: 600;">
            <span>Required Deposit ({proposal.deposit_percent}%):</span>
            <span>${deposit_amount:.2f}</span>
        </div>
        <div class="summary-row" style="color: #64748b;">
            <span>Balance Remaining:</span>
            <span>${balance_amount:.2f}</span>
        </div>
        <div class="summary-row total-row">
            <span>Total Package:</span>
            <span>${proposal.total_amount:.2f}</span>
        </div>
    </div>
</body>
</html>
"""
