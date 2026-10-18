"""Proposal, Invoice, and Payment schemas."""

from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class ProposalCreate(BaseModel):
    deposit_percent: float = 30.0


class ProposalResponse(BaseModel):
    id: str
    event_id: str
    event_title: Optional[str] = None
    client_name: Optional[str] = None
    version: int
    total_amount: float
    deposit_percent: float
    deposit_amount: float = 0.0
    public_token: str
    public_url: Optional[str] = None
    status: str
    pdf_path: Optional[str] = None
    created_at: datetime
    sent_at: Optional[datetime] = None
    approved_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class InvoiceResponse(BaseModel):
    id: str
    event_id: str
    kind: str
    amount: float
    due_date: Optional[date]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class PaymentCheckoutRequest(BaseModel):
    invoice_id: str


class PaymentResponse(BaseModel):
    id: str
    invoice_id: str
    amount: float
    currency: str
    status: str
    paid_at: datetime

    class Config:
        from_attributes = True
