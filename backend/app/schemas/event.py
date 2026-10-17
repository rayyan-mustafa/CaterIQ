"""Event and event item schemas."""

from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class EventItemAdd(BaseModel):
    menu_item_id: str
    quantity: int = 1
    unit_price: Optional[float] = None
    unit_cost: Optional[float] = None


class EventItemResponse(BaseModel):
    id: str
    menu_item_id: str
    menu_item_name: Optional[str] = None
    category: Optional[str] = None
    quantity: int
    unit_price: float
    unit_cost: float
    line_total: float = 0.0

    class Config:
        from_attributes = True


class EventCreate(BaseModel):
    client_id: str
    location_id: Optional[str] = None
    title: str
    event_date: date
    start_time: Optional[str] = "12:00"
    end_time: Optional[str] = "16:00"
    venue_address: Optional[str] = None
    headcount: int = 50
    notes: Optional[str] = None
    items: List[EventItemAdd] = Field(default_factory=list)


class EventUpdate(BaseModel):
    title: Optional[str] = None
    event_date: Optional[date] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    venue_address: Optional[str] = None
    headcount: Optional[int] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class EventResponse(BaseModel):
    id: str
    organization_id: str
    client_id: str
    client_name: Optional[str] = None
    location_id: Optional[str] = None
    location_name: Optional[str] = None
    title: str
    event_date: date
    start_time: Optional[str]
    end_time: Optional[str]
    venue_address: Optional[str]
    headcount: int
    status: str
    notes: Optional[str]
    created_at: datetime
    items: List[EventItemResponse] = Field(default_factory=list)
    total_revenue: float = 0.0
    total_cost: float = 0.0
    projected_profit: float = 0.0
    profit_margin_pct: float = 0.0

    class Config:
        from_attributes = True


class EventStatusUpdate(BaseModel):
    status: str  # lead, proposed, confirmed, completed, cancelled
