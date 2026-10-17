"""Clients CRM router."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.core.dependencies import AuthenticatedContext, get_current_context, require_role
from backend.app.models.billing import Invoice
from backend.app.models.client import Client
from backend.app.models.event import Event
from backend.app.schemas.client import ClientCreate, ClientResponse, ClientUpdate
from backend.app.services.pricing_service import calculate_event_totals

router = APIRouter(prefix="/clients", tags=["Clients CRM"])


@router.get("", response_model=List[ClientResponse])
def list_clients(
    q: Optional[str] = Query(None, description="Search by name, email, or company"),
    ctx: AuthenticatedContext = Depends(get_current_context),
    db: Session = Depends(get_db),
):
    """List and search clients with aggregated event counts and spend."""
    query = db.query(Client).filter(Client.organization_id == ctx.organization_id)
    if q:
        search = f"%{q.strip().lower()}%"
        query = query.filter(
            (Client.name.ilike(search))
            | (Client.email.ilike(search))
            | (Client.company_name.ilike(search))
        )

    clients = query.all()
    results = []
    for c in clients:
        # Calculate spend from events
        total_spend = 0.0
        for ev in c.events:
            rev, _, _, _ = calculate_event_totals(ev)
            total_spend += rev

        resp = ClientResponse(
            id=c.id,
            organization_id=c.organization_id,
            name=c.name,
            email=c.email,
            phone=c.phone,
            company_name=c.company_name,
            notes=c.notes,
            created_at=c.created_at,
            total_events=len(c.events),
            total_spend=round(total_spend, 2),
        )
        results.append(resp)
    return results


@router.post("", response_model=ClientResponse)
def create_client(
    req: ClientCreate,
    ctx: AuthenticatedContext = Depends(require_role(["owner", "manager"])),
    db: Session = Depends(get_db),
):
    """Register a new customer profile."""
    client = Client(
        organization_id=ctx.organization_id,
        name=req.name.strip(),
        email=req.email.lower().strip(),
        phone=req.phone,
        company_name=req.company_name,
        notes=req.notes,
    )
    db.add(client)
    db.commit()
    db.refresh(client)
    return ClientResponse(
        id=client.id,
        organization_id=client.organization_id,
        name=client.name,
        email=client.email,
        phone=client.phone,
        company_name=client.company_name,
        notes=client.notes,
        created_at=client.created_at,
        total_events=0,
        total_spend=0.0,
    )


@router.get("/{client_id}", response_model=ClientResponse)
def get_client(
    client_id: str,
    ctx: AuthenticatedContext = Depends(get_current_context),
    db: Session = Depends(get_db),
):
    """Get single client details."""
    client = (
        db.query(Client)
        .filter(Client.id == client_id, Client.organization_id == ctx.organization_id)
        .first()
    )
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    total_spend = sum(calculate_event_totals(ev)[0] for ev in client.events)
    return ClientResponse(
        id=client.id,
        organization_id=client.organization_id,
        name=client.name,
        email=client.email,
        phone=client.phone,
        company_name=client.company_name,
        notes=client.notes,
        created_at=client.created_at,
        total_events=len(client.events),
        total_spend=round(total_spend, 2),
    )
