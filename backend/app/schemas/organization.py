"""Organization and location schemas."""

from typing import Optional
from pydantic import BaseModel


class LocationBase(BaseModel):
    name: str
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class LocationCreate(LocationBase):
    pass


class LocationResponse(LocationBase):
    id: str
    organization_id: str

    class Config:
        from_attributes = True


class OrganizationResponse(BaseModel):
    id: str
    name: str

    class Config:
        from_attributes = True
