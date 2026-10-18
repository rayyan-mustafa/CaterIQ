"""Locations router for multi-branch caterers."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.core.dependencies import AuthenticatedContext, get_current_context, require_role
from backend.app.models.organization import Location
from backend.app.schemas.organization import LocationCreate, LocationResponse

router = APIRouter(prefix="/locations", tags=["Locations"])


@router.get("", response_model=List[LocationResponse])
def list_locations(
    ctx: AuthenticatedContext = Depends(get_current_context),
    db: Session = Depends(get_db),
):
    """List all kitchen/depot locations for the tenant."""
    return db.query(Location).filter(Location.organization_id == ctx.organization_id).all()


@router.post("", response_model=LocationResponse)
def create_location(
    req: LocationCreate,
    ctx: AuthenticatedContext = Depends(require_role(["owner", "manager"])),
    db: Session = Depends(get_db),
):
    """Add a new kitchen/branch location."""
    loc = Location(
        organization_id=ctx.organization_id,
        name=req.name,
        address=req.address,
        latitude=req.latitude,
        longitude=req.longitude,
    )
    db.add(loc)
    db.commit()
    db.refresh(loc)
    return loc


@router.delete("/{location_id}", status_code=204)
def delete_location(
    location_id: str,
    ctx: AuthenticatedContext = Depends(require_role(["owner"])),
    db: Session = Depends(get_db),
):
    """Delete a location."""
    loc = (
        db.query(Location)
        .filter(Location.id == location_id, Location.organization_id == ctx.organization_id)
        .first()
    )
    if not loc:
        raise HTTPException(status_code=404, detail="Location not found")
    db.delete(loc)
    db.commit()
    return None
