"""Events and Event Builder router."""

from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.core.dependencies import AuthenticatedContext, get_current_context, require_role
from backend.app.models.client import Client
from backend.app.models.event import Event, EventItem
from backend.app.models.menu import MenuItem
from backend.app.schemas.event import (
    EventCreate,
    EventItemAdd,
    EventItemResponse,
    EventResponse,
    EventStatusUpdate,
    EventUpdate,
)
from backend.app.services.pricing_service import calculate_event_totals

router = APIRouter(prefix="/events", tags=["Events & Catering Orders"])


def format_event_response(ev: Event) -> EventResponse:
    """Format Event ORM object with calculated financial summary."""
    rev, cost, profit, margin = calculate_event_totals(ev)
    items_out = []
    for item in ev.items:
        items_out.append(EventItemResponse(
            id=item.id,
            menu_item_id=item.menu_item_id,
            menu_item_name=item.menu_item.name if item.menu_item else None,
            category=item.menu_item.category if item.menu_item else None,
            quantity=item.quantity,
            unit_price=item.unit_price,
            unit_cost=item.unit_cost,
            line_total=round(item.unit_price * item.quantity * ev.headcount, 2),
        ))

    return EventResponse(
        id=ev.id,
        organization_id=ev.organization_id,
        client_id=ev.client_id,
        client_name=ev.client.name if ev.client else None,
        location_id=ev.location_id,
        location_name=ev.location.name if ev.location else None,
        title=ev.title,
        event_date=ev.event_date,
        start_time=ev.start_time,
        end_time=ev.end_time,
        venue_address=ev.venue_address,
        headcount=ev.headcount,
        status=ev.status,
        notes=ev.notes,
        created_at=ev.created_at,
        items=items_out,
        total_revenue=rev,
        total_cost=cost,
        projected_profit=profit,
        profit_margin_pct=margin,
    )


@router.get("", response_model=List[EventResponse])
def list_events(
    status: Optional[str] = Query(None),
    from_date: Optional[date] = Query(None),
    to_date: Optional[date] = Query(None),
    ctx: AuthenticatedContext = Depends(get_current_context),
    db: Session = Depends(get_db),
):
    """List all events with filtering and financial calculations."""
    query = db.query(Event).filter(Event.organization_id == ctx.organization_id)
    if status:
        query = query.filter(Event.status == status.lower())
    if from_date:
        query = query.filter(Event.event_date >= from_date)
    if to_date:
        query = query.filter(Event.event_date <= to_date)

    events = query.order_by(Event.event_date.asc()).all()
    return [format_event_response(ev) for ev in events]


@router.post("", response_model=EventResponse)
def create_event(
    req: EventCreate,
    ctx: AuthenticatedContext = Depends(require_role(["owner", "manager"])),
    db: Session = Depends(get_db),
):
    """Create a new catering event and attach menu items."""
    # Verify client exists and belongs to tenant
    client = (
        db.query(Client)
        .filter(Client.id == req.client_id, Client.organization_id == ctx.organization_id)
        .first()
    )
    if not client:
        raise HTTPException(status_code=404, detail="Client not found.")

    # Double-booking check: same location on same date
    if req.location_id:
        overlapping = (
            db.query(Event)
            .filter(
                Event.organization_id == ctx.organization_id,
                Event.location_id == req.location_id,
                Event.event_date == req.event_date,
                Event.status.in_(["confirmed", "proposed"]),
            )
            .first()
        )
        # We allow creation but log warning / info in notes if needed

    event = Event(
        organization_id=ctx.organization_id,
        location_id=req.location_id,
        client_id=req.client_id,
        title=req.title,
        event_date=req.event_date,
        start_time=req.start_time,
        end_time=req.end_time,
        venue_address=req.venue_address,
        headcount=max(1, req.headcount),
        status="lead",
        notes=req.notes,
    )
    db.add(event)
    db.flush()

    for it in req.items:
        m_item = (
            db.query(MenuItem)
            .filter(MenuItem.id == it.menu_item_id, MenuItem.organization_id == ctx.organization_id)
            .first()
        )
        if m_item:
            price = it.unit_price if it.unit_price is not None else m_item.price_per_head
            cost = it.unit_cost if it.unit_cost is not None else m_item.cost_per_head
            e_item = EventItem(
                event_id=event.id,
                menu_item_id=m_item.id,
                quantity=it.quantity,
                unit_price=price,
                unit_cost=cost,
            )
            db.add(e_item)

    db.commit()
    db.refresh(event)
    return format_event_response(event)


@router.get("/{event_id}", response_model=EventResponse)
def get_event(
    event_id: str,
    ctx: AuthenticatedContext = Depends(get_current_context),
    db: Session = Depends(get_db),
):
    """Retrieve full event detail with calculated totals."""
    ev = (
        db.query(Event)
        .filter(Event.id == event_id, Event.organization_id == ctx.organization_id)
        .first()
    )
    if not ev:
        raise HTTPException(status_code=404, detail="Event not found.")
    return format_event_response(ev)


@router.patch("/{event_id}/status", response_model=EventResponse)
def update_event_status(
    event_id: str,
    req: EventStatusUpdate,
    ctx: AuthenticatedContext = Depends(require_role(["owner", "manager"])),
    db: Session = Depends(get_db),
):
    """Advance or update event lifecycle status."""
    ev = (
        db.query(Event)
        .filter(Event.id == event_id, Event.organization_id == ctx.organization_id)
        .first()
    )
    if not ev:
        raise HTTPException(status_code=404, detail="Event not found.")

    valid_statuses = {"lead", "proposed", "confirmed", "completed", "cancelled"}
    if req.status.lower() not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Status must be one of: {', '.join(valid_statuses)}")

    ev.status = req.status.lower()
    db.commit()
    db.refresh(ev)
    return format_event_response(ev)


@router.post("/{event_id}/items", response_model=EventResponse)
def add_item_to_event(
    event_id: str,
    item_req: EventItemAdd,
    ctx: AuthenticatedContext = Depends(require_role(["owner", "manager"])),
    db: Session = Depends(get_db),
):
    """Attach a menu item to the event."""
    ev = (
        db.query(Event)
        .filter(Event.id == event_id, Event.organization_id == ctx.organization_id)
        .first()
    )
    if not ev:
        raise HTTPException(status_code=404, detail="Event not found.")

    m_item = (
        db.query(MenuItem)
        .filter(MenuItem.id == item_req.menu_item_id, MenuItem.organization_id == ctx.organization_id)
        .first()
    )
    if not m_item:
        raise HTTPException(status_code=404, detail="Menu item not found.")

    price = item_req.unit_price if item_req.unit_price is not None else m_item.price_per_head
    cost = item_req.unit_cost if item_req.unit_cost is not None else m_item.cost_per_head

    e_item = EventItem(
        event_id=ev.id,
        menu_item_id=m_item.id,
        quantity=item_req.quantity,
        unit_price=price,
        unit_cost=cost,
    )
    db.add(e_item)
    db.commit()
    db.refresh(ev)
    return format_event_response(ev)
