"""Client schemas."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class ClientBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    company_name: Optional[str] = None
    notes: Optional[str] = None


class ClientCreate(ClientBase):
    pass


class ClientUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company_name: Optional[str] = None
    notes: Optional[str] = None


class ClientResponse(ClientBase):
    id: str
    organization_id: str
    created_at: datetime
    total_events: int = 0
    total_spend: float = 0.0

    class Config:
        from_attributes = True
