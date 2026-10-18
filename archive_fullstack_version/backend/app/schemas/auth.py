"""Authentication and user schemas."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    organization_name: str


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    organization_id: str
    organization_name: str
    role: str
    full_name: str
    email: str


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class InviteStaffRequest(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    role: str = "staff"  # manager, staff, driver
    location_id: Optional[str] = None
