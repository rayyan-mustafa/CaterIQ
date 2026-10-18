"""Reporting and Financial Analytics router."""

from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.core.dependencies import AuthenticatedContext, get_current_context, require_role
from backend.app.services.reporting_service import (
    export_profit_report_csv,
    get_event_profit_report,
    get_events_report,
    get_outstanding_invoices_report,
    get_revenue_report,
)

router = APIRouter(prefix="/reports", tags=["Reports & Analytics"])


@router.get("/events")
def events_report(
    from_date: Optional[date] = Query(None),
    to_date: Optional[date] = Query(None),
    ctx: AuthenticatedContext = Depends(require_role(["owner", "manager"])),
    db: Session = Depends(get_db),
):
    """Event counts grouped by status."""
    return get_events_report(db, ctx.organization_id, from_date, to_date)


@router.get("/revenue")
def revenue_report(
    from_date: Optional[date] = Query(None),
    to_date: Optional[date] = Query(None),
    ctx: AuthenticatedContext = Depends(require_role(["owner", "manager"])),
    db: Session = Depends(get_db),
):
    """Total paid revenue."""
    return get_revenue_report(db, ctx.organization_id, from_date, to_date)


@router.get("/profit")
def profit_report(
    format: Optional[str] = Query(None, description="Set to 'csv' to download as spreadsheet"),
    from_date: Optional[date] = Query(None),
    to_date: Optional[date] = Query(None),
    ctx: AuthenticatedContext = Depends(require_role(["owner", "manager"])),
    db: Session = Depends(get_db),
):
    """Profit and margin breakdown per event, with optional CSV export."""
    rows = get_event_profit_report(db, ctx.organization_id, from_date, to_date)

    if format and format.lower() == "csv":
        csv_text = export_profit_report_csv(rows)
        return Response(
            content=csv_text,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=cateriq_profit_report.csv"},
        )

    # Compute overall totals
    tot_rev = sum(r["revenue"] for r in rows)
    tot_cost = sum(r["food_cost"] for r in rows)
    tot_profit = sum(r["profit"] for r in rows)
    avg_margin = (tot_profit / tot_rev * 100.0) if tot_rev > 0 else 0.0

    return {
        "summary": {
            "total_revenue": round(tot_rev, 2),
            "total_food_cost": round(tot_cost, 2),
            "net_profit": round(tot_profit, 2),
            "overall_margin_pct": round(avg_margin, 1),
            "events_analyzed": len(rows),
        },
        "events": rows,
    }


@router.get("/outstanding")
def outstanding_report(
    ctx: AuthenticatedContext = Depends(require_role(["owner", "manager"])),
    db: Session = Depends(get_db),
):
    """Aging summary of unpaid invoices."""
    return get_outstanding_invoices_report(db, ctx.organization_id)
