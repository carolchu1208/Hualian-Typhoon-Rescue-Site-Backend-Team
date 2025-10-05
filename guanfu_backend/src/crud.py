from typing import List, Optional, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from . import models
from .schemas import SupplyCreate, SupplyItemDistribution
from .pin_related import generate_pin

ModelType = TypeVar("ModelType", bound=models.Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


def get_by_id(db: Session, model: Type[ModelType], id: str) -> Optional[ModelType]:
    return db.query(model).filter(model.id == id).first()


def get_multi(db: Session, model: Type[ModelType], skip: int = 0, limit: int = 100, **filters) -> List[Type[ModelType]]:
    query = db.query(model)
    if filters:
        query = query.filter_by(**{k: v for k, v in filters.items() if v is not None})
    return query.offset(skip).limit(limit).all()


def count(db: Session, model: Type[ModelType], **filters) -> int:
    query = db.query(model)
    if filters:
        query = query.filter_by(**{k: v for k, v in filters.items() if v is not None})
    return query.count()


def create(db: Session, model: Type[ModelType], obj_in: CreateSchemaType) -> ModelType:
    db_obj = model(**obj_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def create_with_input(db: Session, model: Type[ModelType], obj_in: CreateSchemaType, **kwargs) -> ModelType:
    db_obj = model(**obj_in.model_dump(mode="json"), **kwargs)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(db: Session, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
    update_data = obj_in.model_dump(exclude_unset=True)
    for field in update_data:
        setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


# =====================
# for supply
# =====================

def create_supply_with_items(db: Session, obj_in: SupplyCreate) -> models.Supply:
    """
    建立一個新的供應單 (Supply)，如果請求中包含了第一個物資項目 (SupplyItem)，
    則在同一個資料庫交易中一併建立。
    """
    # 1. 將 Pydantic schema 轉換為字典，並排除掉巢狀的 'supplies' 部分
    supply_data = obj_in.model_dump(exclude={"supplies"})
    nested_item_data = obj_in.supplies

    # 2. 建立主體 Supply 物件的實例
    db_supply = models.Supply(**supply_data, edit_pin=generate_pin())
    db.add(db_supply)

    # 3. 檢查是否有提供第一個物資項目的資料
    if nested_item_data:
        # 4. 建立 SupplyItem 物件的實例
        #    - **nested_item_data.model_dump(): 將巢状 Pydantic 物件轉為字典
        #    - **supply_id=db_supply.id: 關鍵步驟！將剛剛建立的 Supply 物件的 id 關聯過去
        db_item = models.SupplyItem(
            **nested_item_data.model_dump(),
            supply_id=db_supply.id
        )
        db.add(db_item)

    db.commit()

    # 6. 刷新 db_supply 物件，以從資料庫中取得最新的狀態 (包括關聯的 supply_items)
    db.refresh(db_supply)

    return db_supply


def distribute_items(db: Session, supply_id: str, items_to_distribute: List[SupplyItemDistribution]) -> Optional[List[models.SupplyItem]]:
    """
    批次更新指定 supply_id 底下多筆 SupplyItem 的 received_count。
    這是一個原子操作（transaction），若其中任何一筆更新失敗（例如 ID 無效或超出總量），
    整個交易會被回滾以確保資料一致性。

    參數:
        db: SQLAlchemy 的資料庫 Session。
        supply_id: 該批補給單（Supply）的主鍵 ID。
        items_to_distribute: 要更新的項目清單，包含 item 的 id 與要累加的數量。

    回傳:
        成功時回傳更新後的 SupplyItem 物件清單；失敗時回傳 None。
    """

    try:
        # 1. 先整理出所有要更新的 item_ids（使用集合避免重複）
        item_ids_to_update = {item.id for item in items_to_distribute}
        if not item_ids_to_update:
            # 沒有要更新的項目，直接回傳空陣列（視為成功但無操作）
            return []

        # 2. 一次性查出所有相關的 SupplyItem
        #    - 僅限於指定的 supply_id
        #    - 使用 with_for_update() 進行資料列鎖定，避免併發下產生競爭條件（race condition）
        db_items = (
            db.query(models.SupplyItem)
            .filter(
                models.SupplyItem.supply_id == supply_id,
                models.SupplyItem.id.in_(item_ids_to_update),
            )
            .with_for_update()
            .all()
        )

        # 3. 驗證是否所有請求的 item_ids 都存在且屬於該 supply_id
        if len(db_items) != len(item_ids_to_update):
            # 若有任一 item_id 不存在或不屬於該補給單，視為整體失敗
            db.rollback()
            return None

        # 4. 建立快取對照表，加速後續以 id 取物件
        items_map = {str(item.id): item for item in db_items}

        # 5. 逐筆處理更新請求，進行商業邏輯檢核與更新
        for item_update_request in items_to_distribute:
            db_item = items_map.get(str(item_update_request.id))

            # 理論上不會發生（已在第 3 步檢核），此處作為雙重保險
            if not db_item:
                db.rollback()
                return None

            # 6. 商業邏輯檢查：累加後的 received_count 不得超過 total_number
            current_received = db_item.received_count or 0

            # 防禦性檢查：count 不得為負數或是 None
            if item_update_request.count is None or item_update_request.count < 0:
                db.rollback()
                return None

            new_received_count = current_received + item_update_request.count

            if new_received_count > db_item.total_number:
                # 超過需求總量，整筆交易失敗並回滾
                db.rollback()
                return None

            # 7. 寫入累加後的數量
            db_item.received_count = new_received_count

        # 8. 所有檢查皆通過後，提交交易
        db.commit()

        # 9. 回傳更新後的物件清單（此時 db_items 內容已更新）
        return db_items

    except SQLAlchemyError:
        # 例外狀況（例如資料庫連線中斷、鎖定死結等），為確保一致性須回滾
        db.rollback()
        return None
