from typing import List, Optional, Type, TypeVar

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import exists, and_
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session

from . import models
from .schemas import SupplyCreate, SupplyItemDistribution
from .pin_related import generate_pin
from .enum_serializer import *

ModelType = TypeVar("ModelType", bound=models.Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


def get_by_id(db: Session, model: Type[ModelType], id: str) -> Optional[ModelType]:
    return db.query(model).filter(model.id == id).first()


def get_multi(db: Session, model: Type[ModelType], skip: int = 0, limit: int = 100, **filters) -> List[Type[ModelType]]:
    query = db.query(model)
    if filters:
        query = query.filter_by(**normalize_filters_dict(filters))  # Enum to value
    return query.offset(skip).limit(limit).all()


def count(db: Session, model: Type[ModelType], **filters) -> int:
    query = db.query(model)
    if filters:
        query = query.filter_by(**normalize_filters_dict(filters))  # Enum to value
    return query.count()


def create(db: Session, model: Type[ModelType], obj_in: CreateSchemaType) -> ModelType:
    """
    建立一般資料列：
    - 僅在 POST（建立）階段，Pydantic schema 已做正規驗證（例如 status 限制）。
    - 在持久化前，統一將 Enum 轉為字串，避免 psycopg2 適配問題。
    """
    data = normalize_payload_dict(obj_in.model_dump())  # Enum to value
    db_obj = model(**data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def create_with_input(db: Session, model: Type[ModelType], obj_in: CreateSchemaType, **kwargs) -> ModelType:
    """
    建立資料列（帶額外 kwargs）：
    - 同樣進行型別正規化，避免 Enum 直接傳入。
    - obj_in.model_dump(mode="json") 之後再做正規化，確保容器內部的 Enum 也被轉字串。
    """
    payload = normalize_payload_dict(obj_in.model_dump(mode="json"))
    extra = normalize_payload_dict(kwargs) if kwargs else {}
    db_obj = model(**payload, **extra)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(db: Session, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
    """
    更新資料列：
    - 只在 POST 做嚴格驗證；PUT/PATCH 可寬鬆（schema 以 Optional[str] 允許非標準值）。
    - 但仍需避免 Enum 直接進 DB，故在這裡統一轉字串。
    """
    update_data = normalize_payload_dict(obj_in.model_dump(exclude_unset=True))
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


# =====================
# for supply
# =====================

def create_supply_with_items(db: Session, obj_in: SupplyCreate) -> models.Supply:
    """
    建立供應單與其多個物資項目（若提供），在同一個交易中完成。
    - 為 Supply 自動產生 valid_pin
    - 為每個 SupplyItem 套用預設值與基本防呆檢核
    - 正規化 payload，避免 Enum 帶入
    """
    try:
        # 1) 建立 Supply 主體
        supply_data_raw = obj_in.model_dump(exclude={"supplies"}, exclude_unset=True)
        supply_data = normalize_payload_dict(supply_data_raw)  # Enum to value
        db_supply = models.Supply(**supply_data, valid_pin=generate_pin())
        db.add(db_supply)
        db.flush()  # 先拿到 db_supply.id 供 items 關聯

        # 2) 若有 supplies，批量建立
        items_in: List = getattr(obj_in, "supplies", []) or []
        db_items: List[models.SupplyItem] = []

        for idx, item_in in enumerate(items_in, start=1):
            item_data_raw = item_in.model_dump(exclude_unset=True)
            item_data = normalize_payload_dict(item_data_raw)  # Enum to value

            total_number = item_data.get("total_number", None)
            if total_number is None or total_number <= 0:
                raise HTTPException(status_code=400, detail=f"第 {idx} 個物資 total_number 必須是正整數")

            received_count = item_data.get("received_count", 0) or 0
            if received_count < 0:
                raise HTTPException(status_code=400, detail=f"第 {idx} 個物資 received_count 不可為負數")
            if received_count > total_number:
                raise HTTPException(status_code=400, detail=f"第 {idx} 個物資 received_count 不可超過 total_number")

            db_item = models.SupplyItem(
                supply_id=db_supply.id,
                total_number=total_number,
                tag=item_data.get("tag"),
                name=item_data.get("name"),
                received_count=received_count,
                unit=item_data.get("unit"),
            )
            db_items.append(db_item)

        if db_items:
            db.add_all(db_items)

        # 3) 提交交易
        db.commit()

        # 4) 重新載入，帶出關聯
        db.refresh(db_supply)
        return db_supply

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="建立供應單時發生資料完整性錯誤")
    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="建立供應單時發生未預期錯誤")


def distribute_items(db: Session, supply_id: str, items_to_distribute: List[SupplyItemDistribution]) -> Optional[List[models.SupplyItem]]:
    """
    批次更新指定 supply_id 底下多筆 SupplyItem 的 received_count。
    這是一個原子操作（transaction），若其中任何一筆更新失敗（例如 ID 無效或超出總量），
    整個交易會被回滾以確保資料一致性。
    """
    try:
        item_ids_to_update = {item.id for item in items_to_distribute}
        if not item_ids_to_update:
            return []

        db_items = (
            db.query(models.SupplyItem)
            .filter(
                models.SupplyItem.supply_id == supply_id,
                models.SupplyItem.id.in_(item_ids_to_update),
            )
            .with_for_update()
            .all()
        )

        if len(db_items) != len(item_ids_to_update):
            db.rollback()
            return None

        items_map = {str(item.id): item for item in db_items}

        for item_update_request in items_to_distribute:
            db_item = items_map.get(str(item_update_request.id))
            if not db_item:
                db.rollback()
                return None

            current_received = db_item.received_count or 0

            if item_update_request.count is None or item_update_request.count < 0:
                db.rollback()
                return None

            new_received_count = current_received + item_update_request.count

            if new_received_count > db_item.total_number:
                db.rollback()
                return None

            db_item.received_count = new_received_count

        db.commit()
        return db_items

    except SQLAlchemyError:
        db.rollback()
        return None


def get_full_supply(db: Session, query) -> models.Supply:
    not_fulfilled_exists = exists().where(
        and_(
            models.SupplyItem.supply_id == models.Supply.id,
            models.SupplyItem.received_count < models.SupplyItem.total_number
        )
    )
    return query.filter(not_fulfilled_exists)
