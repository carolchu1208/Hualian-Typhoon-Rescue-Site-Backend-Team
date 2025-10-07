from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..database import get_db
from ..enum_serializer import SupplyItemTypeEnum

router = APIRouter(
    prefix="/supply_items",
    tags=["物資項目（Supply Items）"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=schemas.SupplyItemCollection, summary="取得特定供應單物資項目清單")
def list_supply_items(
        supply_id: Optional[str] = Query(None),
        tag: Optional[SupplyItemTypeEnum] = Query(None),
        limit: int = Query(100, ge=1, le=500),
        offset: int = Query(0, ge=0),
        db: Session = Depends(get_db)
):
    """
    取得物資項目清單 (分頁)
    """
    filters = {"supply_id": supply_id, "tag": tag.value if tag else None, }
    items = crud.get_multi(db, models.SupplyItem, skip=offset, limit=limit, **filters)
    total = crud.count(db, models.SupplyItem, **filters)
    return {"member": items, "totalItems": total, "limit": limit, "offset": offset}


@router.post("/", response_model=schemas.SupplyItem, status_code=201, summary="建立特定供應單物資項目")
def create_supply_item(
        item_in: schemas.SupplyItemCreateWithPin, db: Session = Depends(get_db)
):
    """
    建立物資項目
    """
    # Check if parent supply_id exists
    parent_supply = crud.get_by_id(db, models.Supply, id=item_in.supply_id)
    if not parent_supply:
        raise HTTPException(status_code=400, detail=f"supplies with id {item_in.supply_id} does not exist.")
    if parent_supply.valid_pin and parent_supply.valid_pin != item_in.valid_pin:
        raise HTTPException(status_code=400, detail="The PIN you entered is incorrect.")
    if item_in.received_count > item_in.total_number:
        raise HTTPException(status_code=400, detail="Received_count must be less than or equal to total_number.")
    # remove unused columns
    supply_item = item_in.model_dump()
    del supply_item["valid_pin"]
    return crud.create(db, models.SupplyItem, obj_in=schemas.SupplyItemCreate(**supply_item))


@router.patch("/{id}", response_model=schemas.SupplyItem, status_code=200, summary="更新特定供應單物資項目")
def patch_supply_item(
        id: str, item_in: schemas.SupplyItemPatch, db: Session = Depends(get_db)
):
    """
    更新物資項目
    """
    # Check if parent supply_id exists
    db_supply_item = crud.get_by_id(db, models.SupplyItem, id=id)
    if not db_supply_item:
        raise HTTPException(status_code=404, detail="Supply Item not found.")
    if db_supply_item.supply.valid_pin and db_supply_item.supply.valid_pin != item_in.valid_pin:
        raise HTTPException(status_code=400, detail="The PIN you entered is incorrect.")
    # validate num
    if item_in.total_number is not None or item_in.received_count is not None:
        if db_supply_item.total_number == db_supply_item.received_count:
            raise HTTPException(status_code=400, detail="Received_count and total_number are locked because their values are equal; updates are not allowed.")
        total_number = item_in.total_number if item_in.total_number is not None else db_supply_item.total_number
        received_count = item_in.received_count if item_in.received_count is not None else db_supply_item.received_count
        if received_count > total_number:
            raise HTTPException(status_code=400, detail="Received_count must be less than or equal to total_number.")
    return crud.update(db, db_obj=db_supply_item, obj_in=item_in)


@router.get("/{id}", response_model=schemas.SupplyItem, summary="取得特定物資項目")
def get_supply_item(id: str, db: Session = Depends(get_db)):
    """
    取得單一物資項目
    """
    db_item = crud.get_by_id(db, models.SupplyItem, id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Supply Item not found")
    return db_item
