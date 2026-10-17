"""Financial and operational reporting services."""

import csv
from datetime import date, datetime, timezone
import io
from typing import Any, Dict, List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from backend.app.models.billing import Invoice, Payment
from backend.app.models.client import Client
from backend.app.models.event import Event, EventItem
from backend.app.services.pricing_service import calculate_event_totals


def get_events_report(
    db: Session,
    org_id: str,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
) -> Dict[str, Any]:
    """Summary of events by status and location within date range."""
    query = db.query(Event).filter(Event.organization_id == org_id)
    if from_date:
        query = query.filter(Event.event_date >= from_date)
    if to_date:
        query = query.filter(Event.event_date <= to_date)

    events = query.all()
    status_counts: Dict[str, int] = {}
    for ev in events:
        status_counts[ev.status] = status_counts.get(ev.status, 0) + 1

    return {
        "total_events": len(events),
        "status_breakdown": status_counts,
        "from_date": str(from_date) if from_date else None,
        "to_date": str(to_date) if to_date else None,
    }


def get_revenue_report(
    db: Session,
    org_id: str,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
) -> Dict[str, Any]:
    """Sum of paid invoices and payments within date range."""
    query = db.query(Payment).filter(Payment.organization_id == org_id, Payment.status == "succeeded")
    if from_date:
        query = query.filter(func.date(Payment.paid_at) >= from_date)
    if to_date:
        query = query.filter(func.date(Payment.paid_at) <= to_date)

    payments = query.all()
    total_revenue = sum(p.amount for p in payments)

    return {
        "total_revenue": round(total_revenue, 2),
        "payments_count": len(payments),
    }


def get_event_profit_report(
    db: Session,
    org_id: str,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
) -> List[Dict[str, Any]]:
    """Detailed event-by-event profit and margin calculation."""
    query = db.query(Event).filter(Event.organization_id == org_id)
    if from_date:
        query = query.filter(Event.event_date >= from_date)
    if to_date:
        query = query.filter(Event.event_date <= to_date)

    events = query.all()
    rows = []
    for ev in events:
        rev, cost, profit, margin = calculate_event_totals(ev)
        rows.append({
            "event_id": ev.id,
            "title": ev.title,
            "event_date": str(ev.event_date),
            "client_name": ev.client.name if ev.client else "Unknown",
            "headcount": ev.headcount,
            "status": ev.status,
            "revenue": rev,
            "food_cost": cost,
            "profit": profit,
            "margin_pct": margin,
        })
    return rows


def get_outstanding_invoices_report(db: Session, org_id: str) -> Dict[str, Any]:
    """Aging buckets of unpaid invoices (0-30 days, 31-60 days, 60+ days)."""
    unpaid = (
        db.query(Invoice)
        .filter(Invoice.organization_id == org_id, Invoice.status == "unpaid")
        .all()
    )

    today = date.today()
    bucket_0_30 = 0.0
    bucket_31_60 = 0.0
    bucket_60_plus = 0.0
    items = []

    for inv in unpaid:
        due = inv.due_date or today
        days_overdue = (today - due).days if today > due else 0
        if days_overdue <= 30:
            bucket_0_30 += inv.amount
        elif days_overdue <= 60:
            bucket_31_60 += inv.amount
        else:
            bucket_60_plus += inv.amount

        items.append({
            "invoice_id": inv.id,
            "event_id": inv.event_id,
            "event_title": inv.event.title if inv.event else "",
            "kind": inv.kind,
            "amount": inv.amount,
            "due_date": str(inv.due_date),
            "days_overdue": max(0, days_overdue),
        })

    total_unpaid = bucket_0_30 + bucket_31_60 + bucket_60_plus
    return {
        "total_outstanding": round(total_unpaid, 2),
        "buckets": {
            "current_to_30_days": round(bucket_0_30, 2),
            "31_to_60_days": round(bucket_31_60, 2),
            "60_plus_days": round(bucket_60_plus, 2),
        },
        "invoices": items,
    }


def export_profit_report_csv(rows: List[Dict[str, Any]]) -> str:
    """Generate CSV text for profit report."""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Event ID",
        "Title",
        "Date",
        "Client",
        "Headcount",
        "Status",
        "Revenue ($)",
        "Food Cost ($)",
        "Profit ($)",
        "Margin (%)",
    ])
    for r in rows:
        writer.writerow([
            r["event_id"],
            r["title"],
            r["event_date"],
            r["client_name"],
            r["headcount"],
            r["status"],
            r["revenue"],
            r["food_cost"],
            r["profit"],
            r["margin_pct"],
        ])
    return output.getvalue()
