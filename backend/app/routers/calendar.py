"""Calendar events and standard iCal (.ics) subscription router."""

from datetime import date, datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.core.dependencies import AuthenticatedContext, get_current_context
from backend.app.models.event import Event
from backend.app.models.support import CalendarToken

router = APIRouter(prefix="/calendar", tags=["Calendar & Sync"])


@router.get("/events")
def get_calendar_events(
    from_date: Optional[date] = Query(None, alias="from"),
    to_date: Optional[date] = Query(None, alias="to"),
    ctx: AuthenticatedContext = Depends(get_current_context),
    db: Session = Depends(get_db),
):
    """Retrieve events formatted for Month/Week/Day calendar display."""
    query = db.query(Event).filter(Event.organization_id == ctx.organization_id)
    if from_date:
        query = query.filter(Event.event_date >= from_date)
    if to_date:
        query = query.filter(Event.event_date <= to_date)

    events = query.order_by(Event.event_date.asc()).all()
    calendar_entries = []
    for ev in events:
        calendar_entries.append({
            "id": ev.id,
            "title": ev.title,
            "start": f"{ev.event_date}T{ev.start_time or '10:00'}:00",
            "end": f"{ev.event_date}T{ev.end_time or '14:00'}:00",
            "client_name": ev.client.name if ev.client else "",
            "headcount": ev.headcount,
            "status": ev.status,
            "venue": ev.venue_address or "Kitchen",
        })
    return calendar_entries


@router.get("/token")
def get_or_create_calendar_token(
    ctx: AuthenticatedContext = Depends(get_current_context),
    db: Session = Depends(get_db),
):
    """Get the organization's private iCal subscription token."""
    cal_token = (
        db.query(CalendarToken)
        .filter(CalendarToken.organization_id == ctx.organization_id)
        .first()
    )
    if not cal_token:
        cal_token = CalendarToken(organization_id=ctx.organization_id)
        db.add(cal_token)
        db.commit()
        db.refresh(cal_token)

    return {"token": cal_token.token, "feed_url": f"/api/v1/calendar/{cal_token.token}.ics"}


@router.post("/token/rotate")
def rotate_calendar_token(
    ctx: AuthenticatedContext = Depends(get_current_context),
    db: Session = Depends(get_db),
):
    """Revoke previous calendar token and issue a fresh one."""
    cal_token = (
        db.query(CalendarToken)
        .filter(CalendarToken.organization_id == ctx.organization_id)
        .first()
    )
    if cal_token:
        db.delete(cal_token)
        db.flush()

    new_token = CalendarToken(organization_id=ctx.organization_id)
    db.add(new_token)
    db.commit()
    db.refresh(new_token)
    return {"token": new_token.token, "feed_url": f"/api/v1/calendar/{new_token.token}.ics"}


@router.get("/{token}.ics")
def export_ical_feed(token: str, db: Session = Depends(get_db)):
    """Public read-only RFC 5545 iCalendar (.ics) feed for Google/Apple Calendar."""
    cal_token = db.query(CalendarToken).filter(CalendarToken.token == token).first()
    if not cal_token:
        raise HTTPException(status_code=404, detail="Invalid calendar feed token.")

    events = (
        db.query(Event)
        .filter(
            Event.organization_id == cal_token.organization_id,
            Event.status.in_(["confirmed", "completed", "proposed"]),
        )
        .all()
    )

    now_str = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//CaterIQ//Catering Calendar 1.0//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:CaterIQ Events",
    ]

    for ev in events:
        d_str = ev.event_date.strftime("%Y%m%d")
        lines.extend([
            "BEGIN:VEVENT",
            f"UID:event-{ev.id}@cateriq.app",
            f"DTSTAMP:{now_str}",
            f"DTSTART;VALUE=DATE:{d_str}",
            f"DTEND;VALUE=DATE:{d_str}",
            f"SUMMARY:{ev.title} ({ev.headcount} Guests)",
            f"DESCRIPTION:Status: {ev.status}\\nClient: {ev.client.name if ev.client else ''}\\nNotes: {ev.notes or ''}",
            f"LOCATION:{ev.venue_address or 'Catering Kitchen'}",
            f"STATUS:{'CONFIRMED' if ev.status == 'confirmed' else 'TENTATIVE'}",
            "END:VEVENT",
        ])

    lines.append("END:VCALENDAR")
    ics_body = "\r\n".join(lines) + "\r\n"

    return Response(content=ics_body, media_type="text/calendar")
