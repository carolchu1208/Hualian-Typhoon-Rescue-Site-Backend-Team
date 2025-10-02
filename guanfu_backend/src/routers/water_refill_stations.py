from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/water_refill_stations",
    tags=["Water Refill Stations"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=schemas.WaterRefillStationCollection)
def list_water_refill_stations(
        status: Optional[str] = Query(None),
        water_type: Optional[str] = Query(None),
        is_free: Optional[bool] = Query(None),
        accessibility: Optional[bool] = Query(None),
        limit: int = Query(50, ge=1, le=500),
        offset: int = Query(0, ge=0),
        db: Session = Depends(get_db)
):
    """
    取得飲用水補給站清單 (分頁)
    """
    filters = {
        "status": status,
        "water_type": water_type,
        "is_free": is_free,
        "accessibility": accessibility,
    }
    stations = crud.get_multi(db, models.WaterRefillStation, skip=offset, limit=limit, **filters)
    total = crud.count(db, models.WaterRefillStation, **filters)
    return {"member": stations, "totalItems": total, "limit": limit, "offset": offset}


@router.post("/", response_model=schemas.WaterRefillStation, status_code=201)
def create_water_refill_station(
        station_in: schemas.WaterRefillStationCreate, db: Session = Depends(get_db)
):
    """
    建立飲用水補給站
    """
    return crud.create(db, models.WaterRefillStation, obj_in=station_in)


@router.get("/{id}", response_model=schemas.WaterRefillStation)
def get_water_refill_station(id: str, db: Session = Depends(get_db)):
    """
    取得單一飲用水補給站
    """
    db_station = crud.get_by_id(db, models.WaterRefillStation, id)
    if db_station is None:
        raise HTTPException(status_code=404, detail="Water Refill Station not found")
    return db_station


@router.patch("/{id}", response_model=schemas.WaterRefillStation)
def patch_water_refill_station(
        id: str, station_in: schemas.WaterRefillStationPatch, db: Session = Depends(get_db)
):
    """
    更新飲用水補給站 (部分欄位)
    """
    db_station = crud.get_by_id(db, models.WaterRefillStation, id)
    if db_station is None:
        raise HTTPException(status_code=404, detail="Water Refill Station not found")
    return crud.update(db, db_obj=db_station, obj_in=station_in)
