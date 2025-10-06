from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..database import get_db
from ..enum_serializer import ShowerFacilityTypeEnum, ShowerStationStatusEnum

router = APIRouter(
    prefix="/shower_stations",
    tags=["洗澡點（Shower Stations）"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=schemas.ShowerStationCollection, summary="取得洗澡點清單")
def list_shower_stations(
        status: Optional[ShowerStationStatusEnum] = Query(None),
        facility_type: Optional[ShowerFacilityTypeEnum] = Query(None),
        is_free: Optional[bool] = Query(None),
        requires_appointment: Optional[bool] = Query(None),
        limit: int = Query(50, ge=1, le=500),
        offset: int = Query(0, ge=0),
        db: Session = Depends(get_db)
):
    """
    取得洗澡點清單 (分頁)
    """
    filters = {
        "status": status,
        "facility_type": facility_type,
        "is_free": is_free,
        "requires_appointment": requires_appointment,
    }
    stations = crud.get_multi(db, models.ShowerStation, skip=offset, limit=limit, **filters)
    total = crud.count(db, models.ShowerStation, **filters)
    return {"member": stations, "totalItems": total, "limit": limit, "offset": offset}


@router.post("/", response_model=schemas.ShowerStation, status_code=201, summary="建立洗澡點")
def create_shower_station(
        station_in: schemas.ShowerStationCreate, db: Session = Depends(get_db)
):
    """
    建立洗澡點
    """
    return crud.create(db, models.ShowerStation, obj_in=station_in)


@router.get("/{id}", response_model=schemas.ShowerStation, summary="取得特定洗澡點")
def get_shower_station(id: str, db: Session = Depends(get_db)):
    """
    取得單一洗澡點
    """
    db_station = crud.get_by_id(db, models.ShowerStation, id)
    if db_station is None:
        raise HTTPException(status_code=404, detail="Shower Station not found")
    return db_station


@router.patch("/{id}", response_model=schemas.ShowerStation, summary="更新特定洗澡點")
def patch_shower_station(
        id: str, station_in: schemas.ShowerStationPatch, db: Session = Depends(get_db)
):
    """
    更新洗澡點 (部分欄位)
    """
    db_station = crud.get_by_id(db, models.ShowerStation, id)
    if db_station is None:
        raise HTTPException(status_code=404, detail="Shower Station not found")
    return crud.update(db, db_obj=db_station, obj_in=station_in)
