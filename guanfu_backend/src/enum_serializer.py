import enum
from typing import Dict, Any


def normalize_value(value: Any) -> Any:
    """
    將可能出現於 payload/filters 的 Enum 轉為字串 value。
    同時遞迴處理 list 與 dict 內的 Enum。
    目的：避免 psycopg2 can't adapt type 'Enum' 錯誤。
    """
    if isinstance(value, enum.Enum):
        return value.value
    if isinstance(value, list):
        return [normalize_value(v) for v in value]
    if isinstance(value, dict):
        return {k: normalize_value(v) for k, v in value.items()}
    return value


def normalize_payload_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    將 dict 形式的 payload 做型別正規化：
    - Enum -> 字串 value
    - 遞迴處理容器型別
    - 移除 created_at/updated_at（若模型為 DateTime，避免傳整數 timestamp）
    """
    normalized: Dict[str, Any] = {}
    for k, v in data.items():
        normalized[k] = normalize_value(v)
    # 若你的模型使用 DateTime 並由 DB 自動生成，避免自行傳值造成型別衝突
    normalized.pop("created_at", None)
    normalized.pop("updated_at", None)
    return normalized


def normalize_filters_dict(filters: Dict[str, Any]) -> Dict[str, Any]:
    """
    將 filters 內的 Enum 轉字串，並移除 None 值（避免產生無效 filter_by 條件）。
    """
    normalized: Dict[str, Any] = {}
    for k, v in filters.items():
        if v is None:
            continue
        normalized[k] = normalize_value(v)
    return normalized


class ShelterStatusEnum(enum.Enum):
    open = "open"
    full = "full"
    closed = "closed"
    temporary_closed = "temporary_closed"


class MedicalStationTypeEnum(enum.Enum):
    self_organized = "self_organized"
    fixed_point = "fixed_point"
    shelter_medical = "shelter_medical"


class MedicalStationStatusEnum(enum.Enum):
    active = "active"
    temporarily_closed = "temporarily_closed"
    closed = "closed"


class MentalHealthDurationEnum(enum.Enum):
    temporary = "temporary"
    long_term = "long_term"
    both = "both"


class MentalHealthFormatEnum(enum.Enum):
    onsite = "onsite"
    phone = "phone"
    online = "online"
    hybrid = "hybrid"


class MentalHealthResourceStatusEnum(enum.Enum):
    active = "active"
    paused = "paused"
    ended = "ended"


class AccommodationVacancyEnum(enum.Enum):
    available = "available"
    full = "full"
    unknown = "unknown"
    need_confirm = "need_confirm"


class AccommodationStatusEnum(enum.Enum):
    active = "active"
    paused = "paused"
    ended = "ended"


class ShowerFacilityTypeEnum(enum.Enum):
    mobile_shower = "mobile_shower"
    coin_operated = "coin_operated"
    regular_bathroom = "regular_bathroom"


class ShowerStationStatusEnum(enum.Enum):
    active = "active"
    temporarily_closed = "temporarily_closed"
    ended = "ended"


class WaterTypeEnum(enum.Enum):
    drinking_water = "drinking_water"
    bottled_water = "bottled_water"
    filtered_water = "filtered_water"


class WaterRefillStationStatusEnum(enum.Enum):
    active = "active"
    temporarily_unavailable = "temporarily_unavailable"
    ended = "ended"


class RestroomFacilityTypeEnum(enum.Enum):
    mobile_toilet = "mobile_toilet"
    permanent_toilet = "permanent_toilet"
    public_restroom = "public_restroom"


class RestroomStatusEnum(enum.Enum):
    active = "active"
    maintenance = "maintenance"
    out_of_service = "out_of_service"


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


class HumanResourceStatusEnum(enum.Enum):
    active = "active"
    completed = "completed"
    cancelled = "cancelled"


class SupplyItemTypeEnum(enum.Enum):
    food = "food"
    medical_supplies = "medical_supplies"
    groceries = "groceries"
    machinery = "machinery"
    equipment = "equipment"
    plumber = "plumber"
    other = "other"


class VolunteerOrganizationsRegistrationStatusEnum(enum.Enum):
    accepting = "接受中"
    full = "額滿"
    ended = "已結束"


class ReportStatusEnum(enum.Enum):
    # 規格為字串 'true' / 'false'（非布林）
    true = "true"
    false = "false"
