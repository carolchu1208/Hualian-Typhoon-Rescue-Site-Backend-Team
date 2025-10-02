from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import Optional, List
from .. import crud, models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/supplies",
    tags=["Supplies"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=schemas.SupplyCollection)
def list_supplies(
        embed: Optional[str] = Query(None, enum=["all"]),
        limit: int = Query(50, ge=1, le=500),
        offset: int = Query(0, ge=0),
        db: Session = Depends(get_db)
):
    """
    取得供應單清單 (分頁)
    """
    query = db.query(models.Supply)
    if embed == "all":
        query = query.options(joinedload(models.Supply.supply_items))

    total = query.count()
    supplies = query.offset(offset).limit(limit).all()

    return {"member": supplies, "totalItems": total, "limit": limit, "offset": offset}


@router.post("/", response_model=schemas.Supply, status_code=201)
def create_supply(
        supply_in: schemas.SupplyCreate, db: Session = Depends(get_db)
):
    """
    建立供應單 (注意：同時建立 supply_items 的邏輯需在 crud 中客製化)
    """
    # This requires custom logic in crud.py to handle the nested `supplies` object
    return crud.create_supply_with_items(db, obj_in=supply_in)


@router.get("/{id}", response_model=schemas.Supply)
def get_supply(id: str, db: Session = Depends(get_db)):
    """
    取得單一供應單 (包含其所有物資項目)
    """
    db_supply = db.query(models.Supply).options(joinedload(models.Supply.supply_items)).filter(models.Supply.id == id).first()
    if db_supply is None:
        raise HTTPException(status_code=404, detail="Supply not found")
    return db_supply


# OpenAPI spec indicates this endpoint is disabled.
# @router.patch("/{id}", response_model=schemas.Supply)
# def patch_supply(...):

@router.post("/{id}", response_model=List[schemas.SupplyItem])
def distribute_supply_items(
        id: str, items_in: List[schemas.SupplyItemDistribution], db: Session = Depends(get_db)
):
    """
    批次配送 (累加 recieved_count)
    """
    # This is custom logic and requires a dedicated function in crud or a service layer
    updated_items = crud.distribute_items(db=db, supply_id=id, items_to_distribute=items_in)
    if not updated_items:
        raise HTTPException(status_code=400, detail="Invalid item IDs or distribution count exceeds total needed.")
    return updated_items
