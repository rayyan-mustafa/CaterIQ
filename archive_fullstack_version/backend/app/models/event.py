"""Event and EventItem models."""

from datetime import date, datetime, timezone
import uuid
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from backend.app.core.database import Base


def generate_uuid() -> str:
    return str(uuid.uuid4())


class Event(Base):
    __tablename__ = "events"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    location_id = Column(String(36), ForeignKey("locations.id", ondelete="SET NULL"), nullable=True)
    client_id = Column(String(36), ForeignKey("clients.id", ondelete="RESTRICT"), nullable=False, index=True)

    title = Column(String(255), nullable=False)
    event_date = Column(Date, nullable=False, index=True)
    start_time = Column(String(20), nullable=True)  # e.g. "12:00"
    end_time = Column(String(20), nullable=True)    # e.g. "16:00"
    venue_address = Column(String(255), nullable=True)
    venue_latitude = Column(Float, nullable=True)
    venue_longitude = Column(Float, nullable=True)
    headcount = Column(Integer, nullable=False, default=1)
    status = Column(String(50), nullable=False, default="lead")  # lead, proposed, confirmed, completed, cancelled
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    organization = relationship("Organization")
    location = relationship("Location")
    client = relationship("Client", back_populates="events")
    items = relationship("EventItem", back_populates="event", cascade="all, delete-orphan")
    proposals = relationship("Proposal", back_populates="event", cascade="all, delete-orphan")
    invoices = relationship("Invoice", back_populates="event", cascade="all, delete-orphan")


class EventItem(Base):
    __tablename__ = "event_items"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    event_id = Column(String(36), ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True)
    menu_item_id = Column(String(36), ForeignKey("menu_items.id", ondelete="RESTRICT"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Float, nullable=False, default=0.0)
    unit_cost = Column(Float, nullable=False, default=0.0)

    event = relationship("Event", back_populates="items")
    menu_item = relationship("MenuItem")
