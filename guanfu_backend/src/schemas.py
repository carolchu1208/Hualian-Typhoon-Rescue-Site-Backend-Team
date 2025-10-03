from pydantic import BaseModel, Field
from typing import List, Optional, Any
import datetime


# ===================================================================
# 通用基礎模型 (Common Base Models)
# ===================================================================

class Coordinates(BaseModel):
    lat: Optional[float] = None
    lng: Optional[float] = None


class CollectionBase(BaseModel):
    totalItems: int
    limit: int
    offset: int
    member: List[Any]  # 會在各 Collection 中被具體類型覆寫


# ===================================================================
# 志工團體 (Volunteer Organizations)
# ===================================================================

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
    registration_status: Optional[str] = None
    organization_nature: Optional[str] = None
    coordinator: Optional[str] = None
    contact_info: Optional[str] = None
    registration_method: Optional[str] = None
    service_content: Optional[str] = None
    meeting_info: Optional[str] = None
    notes: Optional[str] = None
    image_url: Optional[str] = None


class VolunteerOrganization(VolunteerOrgBase):
    id: str
    last_updated: Optional[datetime.datetime] = None

    class Config:
        from_attributes = True


class VolunteerOrgCollection(CollectionBase):
    member: List[VolunteerOrganization]


# ===================================================================
# 庇護所 (Shelters)
# ===================================================================

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
    link: Optional[str] = None
    capacity: Optional[int] = None
    current_occupancy: Optional[int] = None
    available_spaces: Optional[int] = None
    facilities: Optional[List[str]] = None
    contact_person: Optional[str] = None
    notes: Optional[str] = None
    coordinates: Optional[Coordinates] = None
    opening_hours: Optional[str] = None


class Shelter(ShelterBase):
    id: str
    created_at: int
    updated_at: int

    class Config:
        from_attributes = True


class ShelterCollection(CollectionBase):
    member: List[Shelter]


# ===================================================================
# 醫療站 (Medical Stations)
# ===================================================================

class MedicalStationBase(BaseModel):
    station_type: str
    name: str
    status: str
    location: Optional[str] = None
    detailed_address: Optional[str] = None
    phone: Optional[str] = None
    contact_person: Optional[str] = None
    services: Optional[List[str]] = []
    operating_hours: Optional[str] = None
    equipment: Optional[List[str]] = []
    medical_staff: Optional[int] = None
    daily_capacity: Optional[int] = None
    coordinates: Optional[Coordinates] = None
    affiliated_organization: Optional[str] = None
    notes: Optional[str] = None
    link: Optional[str] = None


class MedicalStationCreate(MedicalStationBase):
    pass


class MedicalStationPatch(BaseModel):
    station_type: Optional[str] = None
    name: Optional[str] = None
    status: Optional[str] = None
    location: Optional[str] = None
    detailed_address: Optional[str] = None
    phone: Optional[str] = None
    contact_person: Optional[str] = None
    services: Optional[List[str]] = None
    operating_hours: Optional[str] = None
    equipment: Optional[List[str]] = None
    medical_staff: Optional[int] = None
    daily_capacity: Optional[int] = None
    coordinates: Optional[Coordinates] = None
    affiliated_organization: Optional[str] = None
    notes: Optional[str] = None
    link: Optional[str] = None


class MedicalStation(MedicalStationBase):
    id: str
    created_at: int
    updated_at: int

    class Config:
        from_attributes = True


class MedicalStationCollection(CollectionBase):
    member: List[MedicalStation]


# ===================================================================
# 心理健康資源 (Mental Health Resources)
# ===================================================================

class MentalHealthResourceBase(BaseModel):
    duration_type: str
    name: str
    service_format: str
    service_hours: str
    contact_info: str
    is_free: bool
    status: str
    emergency_support: bool
    website_url: Optional[str] = None
    target_audience: Optional[List[str]] = []
    specialties: Optional[List[str]] = []
    languages: Optional[List[str]] = []
    location: Optional[str] = None
    coordinates: Optional[Coordinates] = None
    capacity: Optional[int] = None
    waiting_time: Optional[str] = None
    notes: Optional[str] = None


class MentalHealthResourceCreate(MentalHealthResourceBase):
    pass


class MentalHealthResourcePatch(BaseModel):
    duration_type: Optional[str] = None
    name: Optional[str] = None
    service_format: Optional[str] = None
    service_hours: Optional[str] = None
    contact_info: Optional[str] = None
    is_free: Optional[bool] = None
    status: Optional[str] = None
    emergency_support: Optional[bool] = None
    website_url: Optional[str] = None
    target_audience: Optional[List[str]] = None
    specialties: Optional[List[str]] = None
    languages: Optional[List[str]] = None
    location: Optional[str] = None
    coordinates: Optional[Coordinates] = None
    capacity: Optional[int] = None
    waiting_time: Optional[str] = None
    notes: Optional[str] = None


class MentalHealthResource(MentalHealthResourceBase):
    id: str
    created_at: int
    updated_at: int

    class Config:
        from_attributes = True


class MentalHealthResourceCollection(CollectionBase):
    member: List[MentalHealthResource]


# ===================================================================
# 住宿資源 (Accommodations)
# ===================================================================

class AccommodationBase(BaseModel):
    township: str
    name: str
    has_vacancy: str
    available_period: str
    contact_info: str
    address: str
    pricing: str
    status: str
    restrictions: Optional[str] = None
    room_info: Optional[str] = None
    coordinates: Optional[Coordinates] = None
    info_source: Optional[str] = None
    notes: Optional[str] = None
    capacity: Optional[int] = None
    registration_method: Optional[str] = None
    facilities: Optional[List[str]] = []
    distance_to_disaster_area: Optional[str] = None


class AccommodationCreate(AccommodationBase):
    pass


class AccommodationPatch(BaseModel):
    township: Optional[str] = None
    name: Optional[str] = None
    has_vacancy: Optional[str] = None
    available_period: Optional[str] = None
    contact_info: Optional[str] = None
    address: Optional[str] = None
    pricing: Optional[str] = None
    status: Optional[str] = None
    restrictions: Optional[str] = None
    room_info: Optional[str] = None
    coordinates: Optional[Coordinates] = None
    info_source: Optional[str] = None
    notes: Optional[str] = None
    capacity: Optional[int] = None
    registration_method: Optional[str] = None
    facilities: Optional[List[str]] = None
    distance_to_disaster_area: Optional[str] = None


class Accommodation(AccommodationBase):
    id: str
    created_at: int
    updated_at: int

    class Config:
        from_attributes = True


class AccommodationCollection(CollectionBase):
    member: List[Accommodation]


# ===================================================================
# 洗澡點 (Shower Stations)
# ===================================================================

class GenderSchedule(BaseModel):
    male: Optional[List[str]] = []
    female: Optional[List[str]] = []


class ShowerStationBase(BaseModel):
    name: str
    address: str
    facility_type: str
    time_slots: str
    available_period: str
    is_free: bool
    status: str
    requires_appointment: bool
    coordinates: Optional[Coordinates] = None
    phone: Optional[str] = None
    gender_schedule: Optional[GenderSchedule] = None
    capacity: Optional[int] = None
    pricing: Optional[str] = None
    notes: Optional[str] = None
    info_source: Optional[str] = None
    facilities: Optional[List[str]] = []
    distance_to_guangfu: Optional[str] = None
    contact_method: Optional[str] = None


class ShowerStationCreate(ShowerStationBase):
    pass


class ShowerStationPatch(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    facility_type: Optional[str] = None
    time_slots: Optional[str] = None
    available_period: Optional[str] = None
    is_free: Optional[bool] = None
    status: Optional[str] = None
    requires_appointment: Optional[bool] = None
    coordinates: Optional[Coordinates] = None
    phone: Optional[str] = None
    gender_schedule: Optional[GenderSchedule] = None
    capacity: Optional[int] = None
    pricing: Optional[str] = None
    notes: Optional[str] = None
    info_source: Optional[str] = None
    facilities: Optional[List[str]] = None
    distance_to_guangfu: Optional[str] = None
    contact_method: Optional[str] = None


class ShowerStation(ShowerStationBase):
    id: str
    created_at: int
    updated_at: int

    class Config:
        from_attributes = True


class ShowerStationCollection(CollectionBase):
    member: List[ShowerStation]


# ===================================================================
# 飲用水補給站 (Water Refill Stations)
# ===================================================================

class WaterRefillStationBase(BaseModel):
    name: str
    address: str
    water_type: str
    opening_hours: str
    is_free: bool
    status: str
    accessibility: bool
    coordinates: Optional[Coordinates] = None
    phone: Optional[str] = None
    container_required: Optional[str] = None
    daily_capacity: Optional[int] = None
    water_quality: Optional[str] = None
    facilities: Optional[List[str]] = []
    distance_to_disaster_area: Optional[str] = None
    notes: Optional[str] = None
    info_source: Optional[str] = None


class WaterRefillStationCreate(WaterRefillStationBase):
    pass


class WaterRefillStationPatch(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    water_type: Optional[str] = None
    opening_hours: Optional[str] = None
    is_free: Optional[bool] = None
    status: Optional[str] = None
    accessibility: Optional[bool] = None
    coordinates: Optional[Coordinates] = None
    phone: Optional[str] = None
    container_required: Optional[str] = None
    daily_capacity: Optional[int] = None
    water_quality: Optional[str] = None
    facilities: Optional[List[str]] = None
    distance_to_disaster_area: Optional[str] = None
    notes: Optional[str] = None
    info_source: Optional[str] = None


class WaterRefillStation(WaterRefillStationBase):
    id: str
    created_at: int
    updated_at: int

    class Config:
        from_attributes = True


class WaterRefillStationCollection(CollectionBase):
    member: List[WaterRefillStation]


# ===================================================================
# 廁所 (Restrooms)
# ===================================================================

class RestroomBase(BaseModel):
    name: str
    address: str
    facility_type: str
    opening_hours: str
    is_free: bool
    has_water: bool
    has_lighting: bool
    status: str
    coordinates: Optional[Coordinates] = None
    phone: Optional[str] = None
    male_units: Optional[int] = None
    female_units: Optional[int] = None
    unisex_units: Optional[int] = None
    accessible_units: Optional[int] = None
    cleanliness: Optional[str] = None
    last_cleaned: Optional[int] = None
    facilities: Optional[List[str]] = []
    distance_to_disaster_area: Optional[str] = None
    notes: Optional[str] = None
    info_source: Optional[str] = None


class RestroomCreate(RestroomBase):
    pass


class RestroomPatch(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    facility_type: Optional[str] = None
    opening_hours: Optional[str] = None
    is_free: Optional[bool] = None
    has_water: Optional[bool] = None
    has_lighting: Optional[bool] = None
    status: Optional[str] = None
    coordinates: Optional[Coordinates] = None
    phone: Optional[str] = None
    male_units: Optional[int] = None
    female_units: Optional[int] = None
    unisex_units: Optional[int] = None
    accessible_units: Optional[int] = None
    cleanliness: Optional[str] = None
    last_cleaned: Optional[int] = None
    facilities: Optional[List[str]] = None
    distance_to_disaster_area: Optional[str] = None
    notes: Optional[str] = None
    info_source: Optional[str] = None


class Restroom(RestroomBase):
    id: str
    created_at: int
    updated_at: int

    class Config:
        from_attributes = True


class RestroomCollection(CollectionBase):
    member: List[Restroom]


# ===================================================================
# 人力資源 (Human Resources)
# ===================================================================

class HumanResourceBase(BaseModel):
    org: str
    address: str
    phone: str
    status: str
    is_completed: bool
    role_name: str
    role_type: str
    headcount_need: int
    headcount_got: int
    role_status: str
    pii_date: int
    has_medical: Optional[bool] = None
    skills: Optional[List[str]] = []
    certifications: Optional[List[str]] = []
    experience_level: Optional[str] = None
    language_requirements: Optional[List[str]] = []
    headcount_unit: Optional[str] = None
    shift_start_ts: Optional[int] = None
    shift_end_ts: Optional[int] = None
    shift_notes: Optional[str] = None
    assignment_timestamp: Optional[int] = None
    assignment_count: Optional[int] = None
    assignment_notes: Optional[str] = None


class HumanResourceCreate(HumanResourceBase):
    pass


class HumanResourcePatch(BaseModel):
    org: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    status: Optional[str] = None
    is_completed: Optional[bool] = None
    role_name: Optional[str] = None
    role_type: Optional[str] = None
    headcount_need: Optional[int] = None
    headcount_got: Optional[int] = None
    role_status: Optional[str] = None
    pii_date: Optional[int] = None
    has_medical: Optional[bool] = None
    skills: Optional[List[str]] = None
    certifications: Optional[List[str]] = None
    experience_level: Optional[str] = None
    language_requirements: Optional[List[str]] = None
    headcount_unit: Optional[str] = None
    shift_start_ts: Optional[int] = None
    shift_end_ts: Optional[int] = None
    shift_notes: Optional[str] = None
    assignment_timestamp: Optional[int] = None
    assignment_count: Optional[int] = None
    assignment_notes: Optional[str] = None


class HumanResource(HumanResourceBase):
    id: str
    created_at: int
    updated_at: int
    # Read-only summary fields
    total_roles_in_request: Optional[int] = None
    completed_roles_in_request: Optional[int] = None
    pending_roles_in_request: Optional[int] = None

    # ... and other summary fields if they need to be returned

    class Config:
        from_attributes = True


class HumanResourceCollection(CollectionBase):
    member: List[HumanResource]


# ===================================================================
# 物資項目 (Supply Items) & 物資單 (Supplies)
# ===================================================================

# --- SupplyItem ---
class SupplyItemBase(BaseModel):
    total_number: int
    tag: Optional[str] = None
    name: Optional[str] = None
    received_count: Optional[int] = 0
    unit: Optional[str] = None


class SupplyItemCreate(SupplyItemBase):
    supply_id: str


class SupplyItemPatch(BaseModel):
    total_number: Optional[int] = None
    tag: Optional[str] = None
    name: Optional[str] = None
    received_count: Optional[int] = None
    unit: Optional[str] = None


class SupplyItem(SupplyItemBase):
    id: str
    supply_id: str

    class Config:
        from_attributes = True


class SupplyItemCollection(CollectionBase):
    member: List[SupplyItem]


# --- Supply ---
class SupplyBase(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    notes: Optional[str] = None
    pii_date: int


class SupplyCreate(SupplyBase):
    pass


class SupplyPatch(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    notes: Optional[str] = None
    pii_date: Optional[int] = None


class Supply(SupplyBase):
    id: str
    created_at: int
    updated_at: int
    supply_items: List[SupplyItem] = []  # To embed related items

    class Config:
        from_attributes = True


class SupplyCollection(CollectionBase):
    member: List[Supply]


# --- Schema for POST /supplies/{id} endpoint ---
class SupplyItemDistribution(BaseModel):
    id: str  # supply_item ID
    count: int = Field(..., gt=0)  # count must be a positive integer


# ===================================================================
# 回報事件 (Reports)
# ===================================================================

class ReportBase(BaseModel):
    name: str
    location_type: str
    location_id: str
    reason: str
    status: str
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
