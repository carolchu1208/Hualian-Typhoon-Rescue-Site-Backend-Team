from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from .. import crud, models, schemas
from ..database import get_db
from ..schemas import ShelterStatusEnum
router = APIRouter(
    prefix="/shelters",
    tags=["庇護所（Shelters）"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=schemas.ShelterCollection, summary="取得庇護所清單")
def list_shelters(
        status: Optional[ShelterStatusEnum] = Query(None),
        limit: int = Query(50, ge=1, le=500),
        offset: int = Query(0, ge=0),
        db: Session = Depends(get_db)
):
    """
    取得庇護所清單 (分頁)
    """
    filters = {"status": status}
    shelters = crud.get_multi(db, models.Shelter, skip=offset, limit=limit, **filters)
    total = crud.count(db, models.Shelter, **filters)
    return {"member": shelters, "totalItems": total, "limit": limit, "offset": offset}


@router.post("/", response_model=schemas.Shelter, status_code=201, summary="建立庇護所")
def create_shelter(
        shelter_in: schemas.ShelterCreate, db: Session = Depends(get_db)
):
    """
    建立庇護所
    """
    return crud.create(db, models.Shelter, obj_in=shelter_in)


@router.get("/{id}", response_model=schemas.Shelter, summary="取得特定庇護所")
def get_shelter(id: str, db: Session = Depends(get_db)):
    """
    取得單一庇護所
    """
    db_shelter = crud.get_by_id(db, models.Shelter, id)
    if db_shelter is None:
        raise HTTPException(status_code=404, detail="Shelter not found")
    return db_shelter


@router.patch("/{id}", response_model=schemas.Shelter, summary="更新特定庇護所")
def patch_shelter(
        id: str, shelter_in: schemas.ShelterPatch, db: Session = Depends(get_db)
):
    """
    更新庇護所 (部分欄位)
    """
    db_shelter = crud.get_by_id(db, models.Shelter, id)
    if db_shelter is None:
        raise HTTPException(status_code=404, detail="Shelter not found")
    return crud.update(db, db_obj=db_shelter, obj_in=shelter_in)
