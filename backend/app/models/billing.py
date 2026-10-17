"""Proposals, Invoices, and Payments models."""

from datetime import date, datetime, timezone
import secrets
import uuid
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from backend.app.core.database import Base


def generate_uuid() -> str:
    return str(uuid.uuid4())


def generate_token() -> str:
    return secrets.token_urlsafe(24)


class Proposal(Base):
    __tablename__ = "proposals"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    event_id = Column(String(36), ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True)
    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    version = Column(Integer, default=1, nullable=False)
    total_amount = Column(Float, nullable=False, default=0.0)
    deposit_percent = Column(Float, default=30.0)  # e.g. 30% deposit
    public_token = Column(String(64), unique=True, index=True, default=generate_token, nullable=False)
    status = Column(String(50), default="draft")  # draft, sent, approved, declined
    pdf_path = Column(String(255), nullable=True)
    sent_at = Column(DateTime, nullable=True)
    approved_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    event = relationship("Event", back_populates="proposals")


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    event_id = Column(String(36), ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True)
    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    kind = Column(String(50), default="deposit")  # deposit, balance, full
    amount = Column(Float, nullable=False, default=0.0)
    due_date = Column(Date, nullable=True)
    status = Column(String(50), default="unpaid")  # unpaid, paid, void
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    event = relationship("Event", back_populates="invoices")
    payments = relationship("Payment", back_populates="invoice", cascade="all, delete-orphan")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    invoice_id = Column(String(36), ForeignKey("invoices.id", ondelete="CASCADE"), nullable=False, index=True)
    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    stripe_payment_intent_id = Column(String(255), nullable=True)
    amount = Column(Float, nullable=False, default=0.0)
    currency = Column(String(10), default="usd")
    status = Column(String(50), default="succeeded")
    paid_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    raw_event_id = Column(String(255), unique=True, nullable=True, index=True)  # webhook idempotency key

    invoice = relationship("Invoice", back_populates="payments")
