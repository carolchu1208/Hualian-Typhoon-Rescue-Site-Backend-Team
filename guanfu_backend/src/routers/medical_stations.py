from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from .. import crud, models, schemas
from ..database import get_db
from ..enum_serializer import MedicalStationTypeEnum, MedicalStationStatusEnum

router = APIRouter(
    prefix="/medical_stations",
    tags=["醫療站（Medical Stations）"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=schemas.MedicalStationCollection, summary="取得醫療站清單")
def list_medical_stations(
        status: Optional[MedicalStationStatusEnum] = Query(None),
        station_type: Optional[MedicalStationTypeEnum] = Query(None),
        limit: int = Query(50, ge=1, le=500),
        offset: int = Query(0, ge=0),
        db: Session = Depends(get_db)
):
    """
    取得醫療站清單 (分頁)
    """
    filters = {"status": status, "station_type": station_type}
    stations = crud.get_multi(db, models.MedicalStation, skip=offset, limit=limit, **filters)
    total = crud.count(db, models.MedicalStation, **filters)
    return {"member": stations, "totalItems": total, "limit": limit, "offset": offset}


@router.post("/", response_model=schemas.MedicalStation, status_code=201, summary="建立醫療站")
def create_medical_station(
        station_in: schemas.MedicalStationCreate, db: Session = Depends(get_db)
):
    """
    建立醫療站
    """
    return crud.create(db, models.MedicalStation, obj_in=station_in)


@router.get("/{id}", response_model=schemas.MedicalStation, summary="取得特定醫療站")
def get_medical_station(id: str, db: Session = Depends(get_db)):
    """
    取得單一醫療站
    """
    db_station = crud.get_by_id(db, models.MedicalStation, id)
    if db_station is None:
        raise HTTPException(status_code=404, detail="Medical Station not found")
    return db_station


@router.patch("/{id}", response_model=schemas.MedicalStation, summary="更新特定醫療站")
def patch_medical_station(
        id: str, station_in: schemas.MedicalStationPatch, db: Session = Depends(get_db)
):
    """
    更新醫療站 (部分欄位)
    """
    db_station = crud.get_by_id(db, models.MedicalStation, id)
    if db_station is None:
        raise HTTPException(status_code=404, detail="Medical Station not found")
    return crud.update(db, db_obj=db_station, obj_in=station_in)
