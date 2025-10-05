import enum
import uuid
import time
from sqlalchemy import (
    Column, String, DateTime, Integer, Boolean, Text, BigInteger, ForeignKey, Enum
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


def generate_uuid_str():
    """Generates a string representation of a UUID4."""
    return str(uuid.uuid4())


def current_timestamp_int():
    """Returns the current Unix timestamp as an integer."""
    return int(time.time())


class ShelterStatusEnum(enum.Enum):
    open = "open"
    full = "full"
    closed = "closed"
    temporary_closed = "temporary_closed"


class MedicalStationTypeEnum(enum.Enum):
    self_organized = "self_organized"
    fixed_point = "fixed_point"
    shelter_medical = "shelter_medical"


class GeneralStatusEnum(enum.Enum):
    active = "active"
    paused = "paused"
    ended = "ended"
    temporarily_closed = "temporarily_closed"
    temporarily_unavailable = "temporarily_unavailable"
    maintenance = "maintenance"
    out_of_service = "out_of_service"
    completed = "completed"
    cancelled = "cancelled"


class MentalHealthDurationEnum(enum.Enum):
    temporary = "temporary"
    long_term = "long_term"
    both = "both"


class MentalHealthFormatEnum(enum.Enum):
    onsite = "onsite"
    phone = "phone"
    online = "online"
    hybrid = "hybrid"


class AccommodationVacancyEnum(enum.Enum):
    available = "available"
    full = "full"
    unknown = "unknown"
    need_confirm = "need_confirm"


class ShowerFacilityTypeEnum(enum.Enum):
    mobile_shower = "mobile_shower"
    coin_operated = "coin_operated"
    regular_bathroom = "regular_bathroom"


class WaterTypeEnum(enum.Enum):
    drinking_water = "drinking_water"
    bottled_water = "bottled_water"
    filtered_water = "filtered_water"


class RestroomFacilityTypeEnum(enum.Enum):
    mobile_toilet = "mobile_toilet"
    permanent_toilet = "permanent_toilet"
    public_restroom = "public_restroom"


class HumanResourceRoleTypeEnum(enum.Enum):
    general_volunteer = "general_volunteer"
    medical_staff = "medical_staff"
    logistics = "logistics"
    cleaning = "cleaning"
    admin_support = "admin_support"
    driver = "driver"
    security = "security"
    professional = "professional"
    other = "other"


class HumanResourceRoleStatusEnum(enum.Enum):
    completed = "completed"
    pending = "pending"
    partial = "partial"


class HumanResourceExperienceLevelEnum(enum.Enum):
    level_1 = "level_1"
    level_2 = "level_2"
    level_3 = "level_3"


class SupplyItemTypeEnum(enum.Enum):
    food = "food"
    medical_supplies = "medical_supplies"
    groceries = "groceries"
    machinery = "machinery"
    equipment = "equipment"
    plumber = "plumber"
    other = "other"


# ===================================================================
# 資料表模型定義
# ===================================================================

class VolunteerOrganization(Base):
    __tablename__ = "volunteer_organizations"
    id = Column(String, primary_key=True, default=generate_uuid_str)
    last_updated = Column(DateTime, default=func.now(), onupdate=func.now())
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


class Shelter(Base):
    __tablename__ = "shelters"
    id = Column(String, primary_key=True, default=generate_uuid_str)
    created_at = Column(BigInteger, nullable=False, default=current_timestamp_int)
    updated_at = Column(BigInteger, nullable=False, default=current_timestamp_int, onupdate=current_timestamp_int)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    link = Column(String)
    status = Column(Enum(ShelterStatusEnum), nullable=False)
    capacity = Column(Integer)
    current_occupancy = Column(Integer)
    available_spaces = Column(Integer)
    facilities = Column(JSONB)
    contact_person = Column(String)
    notes = Column(Text)
    coordinates = Column(JSONB)
    opening_hours = Column(String)


class MedicalStation(Base):
    __tablename__ = "medical_stations"
    id = Column(String, primary_key=True, default=generate_uuid_str)
    created_at = Column(BigInteger, nullable=False, default=current_timestamp_int)
    updated_at = Column(BigInteger, nullable=False, default=current_timestamp_int, onupdate=current_timestamp_int)
    station_type = Column(Enum(MedicalStationTypeEnum), nullable=False)
    name = Column(String, nullable=False)
    status = Column(Enum(GeneralStatusEnum), nullable=False)
    location = Column(String)
    detailed_address = Column(String)
    phone = Column(String)
    contact_person = Column(String)
    services = Column(JSONB)
    operating_hours = Column(String)
    equipment = Column(JSONB)
    medical_staff = Column(Integer)
    daily_capacity = Column(Integer)
    coordinates = Column(JSONB)
    affiliated_organization = Column(String)
    notes = Column(Text)
    link = Column(String)


class MentalHealthResource(Base):
    __tablename__ = "mental_health_resources"
    id = Column(String, primary_key=True, default=generate_uuid_str)
    created_at = Column(BigInteger, nullable=False, default=current_timestamp_int)
    updated_at = Column(BigInteger, nullable=False, default=current_timestamp_int, onupdate=current_timestamp_int)
    duration_type = Column(Enum(MentalHealthDurationEnum), nullable=False)
    name = Column(String, nullable=False)
    service_format = Column(Enum(MentalHealthFormatEnum), nullable=False)
    service_hours = Column(String, nullable=False)
    contact_info = Column(String, nullable=False)
    is_free = Column(Boolean, nullable=False)
    status = Column(Enum(GeneralStatusEnum), nullable=False)
    emergency_support = Column(Boolean, nullable=False)
    website_url = Column(String)
    target_audience = Column(JSONB)
    specialties = Column(JSONB)
    languages = Column(JSONB)
    location = Column(String)
    coordinates = Column(JSONB)
    capacity = Column(Integer)
    waiting_time = Column(String)
    notes = Column(Text)


class Accommodation(Base):
    __tablename__ = "accommodations"
    id = Column(String, primary_key=True, default=generate_uuid_str)
    created_at = Column(BigInteger, nullable=False, default=current_timestamp_int)
    updated_at = Column(BigInteger, nullable=False, default=current_timestamp_int, onupdate=current_timestamp_int)
    township = Column(String, nullable=False)
    name = Column(String, nullable=False)
    has_vacancy = Column(Enum(AccommodationVacancyEnum), nullable=False)
    available_period = Column(String, nullable=False)
    contact_info = Column(String, nullable=False)
    address = Column(String, nullable=False)
    pricing = Column(String, nullable=False)
    status = Column(Enum(GeneralStatusEnum), nullable=False)
    restrictions = Column(String)
    room_info = Column(String)
    coordinates = Column(JSONB)
    info_source = Column(String)
    notes = Column(Text)
    capacity = Column(Integer)
    registration_method = Column(String)
    facilities = Column(JSONB)
    distance_to_disaster_area = Column(String)


class ShowerStation(Base):
    __tablename__ = "shower_stations"
    id = Column(String, primary_key=True, default=generate_uuid_str)
    created_at = Column(BigInteger, nullable=False, default=current_timestamp_int)
    updated_at = Column(BigInteger, nullable=False, default=current_timestamp_int, onupdate=current_timestamp_int)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    facility_type = Column(Enum(ShowerFacilityTypeEnum), nullable=False)
    time_slots = Column(String, nullable=False)
    available_period = Column(String, nullable=False)
    is_free = Column(Boolean, nullable=False)
    status = Column(Enum(GeneralStatusEnum), nullable=False)
    requires_appointment = Column(Boolean, nullable=False)
    coordinates = Column(JSONB)
    phone = Column(String)
    gender_schedule = Column(JSONB)
    capacity = Column(Integer)
    pricing = Column(String)
    notes = Column(Text)
    info_source = Column(String)
    facilities = Column(JSONB)
    distance_to_guangfu = Column(String)
    contact_method = Column(String)


class WaterRefillStation(Base):
    __tablename__ = "water_refill_stations"
    id = Column(String, primary_key=True, default=generate_uuid_str)
    created_at = Column(BigInteger, nullable=False, default=current_timestamp_int)
    updated_at = Column(BigInteger, nullable=False, default=current_timestamp_int, onupdate=current_timestamp_int)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    water_type = Column(Enum(WaterTypeEnum), nullable=False)
    opening_hours = Column(String, nullable=False)
    is_free = Column(Boolean, nullable=False)
    status = Column(Enum(GeneralStatusEnum), nullable=False)
    accessibility = Column(Boolean, nullable=False)
    coordinates = Column(JSONB)
    phone = Column(String)
    container_required = Column(String)
    daily_capacity = Column(Integer)
    water_quality = Column(String)
    facilities = Column(JSONB)
    distance_to_disaster_area = Column(String)
    notes = Column(Text)
    info_source = Column(String)


class Restroom(Base):
    __tablename__ = "restrooms"
    id = Column(String, primary_key=True, default=generate_uuid_str)
    created_at = Column(BigInteger, nullable=False, default=current_timestamp_int)
    updated_at = Column(BigInteger, nullable=False, default=current_timestamp_int, onupdate=current_timestamp_int)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    facility_type = Column(Enum(RestroomFacilityTypeEnum), nullable=False)
    opening_hours = Column(String, nullable=False)
    is_free = Column(Boolean, nullable=False)
    has_water = Column(Boolean, nullable=False)
    has_lighting = Column(Boolean, nullable=False)
    status = Column(Enum(GeneralStatusEnum), nullable=False)
    coordinates = Column(JSONB)
    phone = Column(String)
    male_units = Column(Integer)
    female_units = Column(Integer)
    unisex_units = Column(Integer)
    accessible_units = Column(Integer)
    cleanliness = Column(String)
    last_cleaned = Column(BigInteger)
    facilities = Column(JSONB)
    distance_to_disaster_area = Column(String)
    notes = Column(Text)
    info_source = Column(String)


class HumanResource(Base):
    __tablename__ = "human_resources"
    id = Column(String, primary_key=True, default=generate_uuid_str)
    created_at = Column(BigInteger, nullable=False, default=current_timestamp_int)
    updated_at = Column(BigInteger, nullable=False, default=current_timestamp_int, onupdate=current_timestamp_int)
    org = Column(String, nullable=False)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    status = Column(Enum(GeneralStatusEnum), nullable=False)
    is_completed = Column(Boolean, nullable=False)
    role_name = Column(String, nullable=False)
    role_type = Column(Enum(HumanResourceRoleTypeEnum), nullable=False)
    headcount_need = Column(Integer, nullable=False)
    headcount_got = Column(Integer, nullable=False)
    role_status = Column(Enum(HumanResourceRoleStatusEnum), nullable=False)
    has_medical = Column(Boolean)
    skills = Column(JSONB)
    certifications = Column(JSONB)
    experience_level = Column(Enum(HumanResourceExperienceLevelEnum))  # Could be an Enum if levels are fixed
    language_requirements = Column(JSONB)
    headcount_unit = Column(String)
    shift_start_ts = Column(BigInteger)
    shift_end_ts = Column(BigInteger)
    shift_notes = Column(Text)
    assignment_timestamp = Column(BigInteger)
    assignment_count = Column(Integer)
    assignment_notes = Column(Text)
    pii_date = Column(BigInteger, nullable=False, default=current_timestamp_int)
    edit_pin = Column(String)


class Supply(Base):
    __tablename__ = "supplies"
    id = Column(String, primary_key=True, default=generate_uuid_str)
    created_at = Column(BigInteger, nullable=False, default=current_timestamp_int)
    updated_at = Column(BigInteger, nullable=False, default=current_timestamp_int, onupdate=current_timestamp_int)
    name = Column(String)
    address = Column(String)
    phone = Column(String)
    notes = Column(Text)
    supplies = relationship("SupplyItem", back_populates="supply", cascade="all, delete-orphan")
    pii_date = Column(BigInteger, nullable=False, default=current_timestamp_int)
    edit_pin = Column(String)


class SupplyItem(Base):
    __tablename__ = "supply_items"
    id = Column(String, primary_key=True, default=generate_uuid_str)
    supply_id = Column(String, ForeignKey("supplies.id"), nullable=False)
    total_number = Column(Integer, nullable=False)
    tag = Column(Enum(SupplyItemTypeEnum), nullable=False)
    name = Column(String)
    received_count = Column(Integer)
    unit = Column(String)
    supply = relationship("Supply", back_populates="supplies")


class Report(Base):
    __tablename__ = "reports"
    id = Column(String, primary_key=True, default=generate_uuid_str)
    created_at = Column(BigInteger, nullable=False, default=current_timestamp_int)
    updated_at = Column(BigInteger, nullable=False, default=current_timestamp_int, onupdate=current_timestamp_int)
    location_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    location_type = Column(String, nullable=False)
    reason = Column(Text, nullable=False)
    notes = Column(Text)
    status = Column(Boolean, nullable=False)
