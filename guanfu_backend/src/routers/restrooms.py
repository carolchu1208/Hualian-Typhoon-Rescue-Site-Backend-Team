from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from .. import crud, models, schemas
from ..database import get_db
from ..enum_serializer import RestroomFacilityTypeEnum, RestroomStatusEnum

router = APIRouter(
    prefix="/restrooms",
    tags=["廁所點（Restrooms）"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=schemas.RestroomCollection, summary="取得廁所點清單")
def list_restrooms(
        status: Optional[RestroomStatusEnum] = Query(None),
        facility_type: Optional[RestroomFacilityTypeEnum] = Query(None),
        is_free: Optional[bool] = Query(None),
        has_water: Optional[bool] = Query(None),
        has_lighting: Optional[bool] = Query(None),
        limit: int = Query(50, ge=1, le=500),
        offset: int = Query(0, ge=0),
        db: Session = Depends(get_db)
):
    """
    取得廁所點清單 (分頁)
    """
    filters = {
        "status": status,
        "facility_type": facility_type,
        "is_free": is_free,
        "has_water": has_water,
        "has_lighting": has_lighting,
    }
    restrooms = crud.get_multi(db, models.Restroom, skip=offset, limit=limit, **filters)
    total = crud.count(db, models.Restroom, **filters)
    return {"member": restrooms, "totalItems": total, "limit": limit, "offset": offset}


@router.post("/", response_model=schemas.Restroom, status_code=201, summary="建立廁所點")
def create_restroom(
        restroom_in: schemas.RestroomCreate, db: Session = Depends(get_db)
):
    """
    建立廁所點
    """
    return crud.create(db, models.Restroom, obj_in=restroom_in)


@router.get("/{id}", response_model=schemas.Restroom, summary="取得特定廁所點")
def get_restroom(id: str, db: Session = Depends(get_db)):
    """
    取得單一廁所點
    """
    db_restroom = crud.get_by_id(db, models.Restroom, id)
    if db_restroom is None:
        raise HTTPException(status_code=404, detail="Restroom not found")
    return db_restroom


@router.patch("/{id}", response_model=schemas.Restroom, summary="更新特定廁所點")
def patch_restroom(
        id: str, restroom_in: schemas.RestroomPatch, db: Session = Depends(get_db)
):
    """
    更新廁所點 (部分欄位)
    """
    db_restroom = crud.get_by_id(db, models.Restroom, id)
    if db_restroom is None:
        raise HTTPException(status_code=404, detail="Restroom not found")
    return crud.update(db, db_obj=db_restroom, obj_in=restroom_in)
