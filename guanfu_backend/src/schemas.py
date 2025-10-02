# src/schemas.py

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import datetime


# --- Base Schemas ---
class Coordinates(BaseModel):
    lat: Optional[float] = None
    lng: Optional[float] = None


class CollectionBase(BaseModel):
    totalItems: int
    limit: int
    offset: int


# --- Shelter Schemas ---
class ShelterBase(BaseModel):
    name: str
    location: str
    phone: str
    status: str
    link: Optional[str] = None
    capacity: Optional[int] = None
    current_occupancy: Optional[int] = None
    available_spaces: Optional[int] = None
    facilities: Optional[List[str]] = []
    contact_person: Optional[str] = None
    notes: Optional[str] = None
    coordinates: Optional[Coordinates] = None
    opening_hours: Optional[str] = None


class ShelterCreate(ShelterBase):
    pass


class ShelterPatch(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    phone: Optional[str] = None
    status: Optional[str] = None


class Shelter(ShelterBase):
    id: str
    created_at: int
    updated_at: int

    class Config:
        from_attributes = True


class ShelterCollection(CollectionBase):
    member: List[Shelter]


# --- Volunteer Organization Schemas ---
class VolunteerOrgBase(BaseModel):
    organization_name: str
    registration_status: Optional[str] = None
    organization_nature: Optional[str] = None
    coordinator: Optional[str] = None
    contact_info: Optional[str] = None
    registration_method: Optional[str] = None
    service_content: Optional[str] = None
    meeting_info: Optional[str] = None
    notes: Optional[str] = None
    image_url: Optional[str] = None


class VolunteerOrgCreate(VolunteerOrgBase):
    pass


class VolunteerOrgPatch(BaseModel):
    organization_name: Optional[str] = None


class VolunteerOrganization(VolunteerOrgBase):
    id: str
    last_updated: Optional[datetime.datetime] = None

    class Config:
        from_attributes = True


class VolunteerOrgCollection(CollectionBase):
    member: List[VolunteerOrganization]


# --- Report Schemas ---
class ReportBase(BaseModel):
    name: str
    location_type: str
    location_id: str
    reason: str
    status: str  # "true" or "false"
    notes: Optional[str] = None


class ReportCreate(ReportBase):
    pass


class ReportPatch(BaseModel):
    name: Optional[str] = None
    location_type: Optional[str] = None
    location_id: Optional[str] = None
    reason: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class Report(ReportBase):
    id: str
    created_at: int
    updated_at: int

    class Config:
        from_attributes = True


class ReportCollection(CollectionBase):
    member: List[Report]

# Todo: 請繼續為其他資源 (MedicalStation, Accommodation 等) 建立對應的 Schema
