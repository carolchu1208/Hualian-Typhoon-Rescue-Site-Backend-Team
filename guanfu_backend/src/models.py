from sqlalchemy import (
    Column, String, DateTime, Integer, Boolean, Text, BigInteger
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from .database import Base


# --- Volunteer Organizations ---
class VolunteerOrganization(Base):
    __tablename__ = "volunteer_organizations"
    id = Column(String, primary_key=True)
    last_updated = Column(DateTime, onupdate=func.now())
    registration_status = Column(String)
    organization_nature = Column(String)
    organization_name = Column(String, nullable=False)
    coordinator = Column(String)
    contact_info = Column(String)
    registration_method = Column(String)
    service_content = Column(Text)
    meeting_info = Column(Text)
    notes = Column(Text)
    image_url = Column(String)


# --- Shelters ---
class Shelter(Base):
    __tablename__ = "shelters"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    link = Column(String)
    status = Column(String, nullable=False)
    capacity = Column(Integer)
    current_occupancy = Column(Integer)
    available_spaces = Column(Integer)
    facilities = Column(JSONB)  # 使用 JSONB 以獲得更佳的效能和功能
    contact_person = Column(String)
    notes = Column(Text)
    coordinates = Column(JSONB)
    opening_hours = Column(String)
    created_at = Column(BigInteger, nullable=False)
    updated_at = Column(BigInteger, nullable=False)
