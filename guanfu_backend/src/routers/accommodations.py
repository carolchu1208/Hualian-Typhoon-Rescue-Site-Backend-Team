from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from .. import crud, models, schemas
from ..database import get_db
from ..enum_serializer import AccommodationVacancyEnum, AccommodationStatusEnum

router = APIRouter(
    prefix="/accommodations",
    tags=["住宿資源（Accommodations）"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=schemas.AccommodationCollection, summary="取得庇護所清單")
def list_accommodations(
        status: Optional[AccommodationStatusEnum] = Query(None),
        township: Optional[str] = Query(None),
        has_vacancy: Optional[AccommodationVacancyEnum] = Query(None),
        limit: int = Query(50, ge=1, le=500),
        offset: int = Query(0, ge=0),
        db: Session = Depends(get_db)
):
    """
    取得住宿資源清單 (分頁)
    """
    filters = {
        "status": status,
        "township": township,
        "has_vacancy": has_vacancy,
    }
    accommodations = crud.get_multi(db, models.Accommodation, skip=offset, limit=limit, **filters)
    total = crud.count(db, models.Accommodation, **filters)
    return {"member": accommodations, "totalItems": total, "limit": limit, "offset": offset}


@router.post("/", response_model=schemas.Accommodation, status_code=201, summary="建立庇護所")
def create_accommodation(
        accommodation_in: schemas.AccommodationCreate, db: Session = Depends(get_db)
):
    """
    建立住宿資源
    """
    return crud.create(db, models.Accommodation, obj_in=accommodation_in)


@router.get("/{id}", response_model=schemas.Accommodation, summary="取得特定庇護所")
def get_accommodation(id: str, db: Session = Depends(get_db)):
    """
    取得單一住宿資源
    """
    db_accommodation = crud.get_by_id(db, models.Accommodation, id)
    if db_accommodation is None:
        raise HTTPException(status_code=404, detail="Accommodation not found")
    return db_accommodation


@router.patch("/{id}", response_model=schemas.Accommodation, summary="更新特定庇護所資料")
def patch_accommodation(
        id: str, accommodation_in: schemas.AccommodationPatch, db: Session = Depends(get_db)
):
    """
    更新住宿資源 (部分欄位)
    """
    db_accommodation = crud.get_by_id(db, models.Accommodation, id)
    if db_accommodation is None:
        raise HTTPException(status_code=404, detail="Accommodation not found")
    return crud.update(db, db_obj=db_accommodation, obj_in=accommodation_in)
