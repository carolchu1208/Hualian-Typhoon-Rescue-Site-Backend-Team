from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from .. import crud, models, schemas
from ..database import get_db
from ..enum_serializer import MentalHealthDurationEnum, MentalHealthFormatEnum, MentalHealthResourceStatusEnum

router = APIRouter(
    prefix="/mental_health_resources",
    tags=["心理健康資源（Mental Health Resources）"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=schemas.MentalHealthResourceCollection, summary="取得心理健康資源清單")
def list_mental_health_resources(
        status: Optional[MentalHealthResourceStatusEnum] = Query(None),
        duration_type: Optional[MentalHealthDurationEnum] = Query(None),
        service_format: Optional[MentalHealthFormatEnum] = Query(None),
        limit: int = Query(50, ge=1, le=500),
        offset: int = Query(0, ge=0),
        db: Session = Depends(get_db)
):
    """
    取得心理健康資源清單 (分頁)
    """
    filters = {
        "status": status,
        "duration_type": duration_type,
        "service_format": service_format,
    }
    resources = crud.get_multi(db, models.MentalHealthResource, skip=offset, limit=limit, **filters)
    total = crud.count(db, models.MentalHealthResource, **filters)
    return {"member": resources, "totalItems": total, "limit": limit, "offset": offset}


@router.post("/", response_model=schemas.MentalHealthResource, status_code=201, summary="建立心理健康資源")
def create_mental_health_resource(
        resource_in: schemas.MentalHealthResourceCreate, db: Session = Depends(get_db)
):
    """
    建立心理健康資源
    """
    return crud.create(db, models.MentalHealthResource, obj_in=resource_in)


@router.get("/{id}", response_model=schemas.MentalHealthResource, summary="取得特定心理健康資源")
def get_mental_health_resource(id: str, db: Session = Depends(get_db)):
    """
    取得單一心理健康資源
    """
    db_resource = crud.get_by_id(db, models.MentalHealthResource, id)
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Mental Health Resource not found")
    return db_resource


@router.patch("/{id}", response_model=schemas.MentalHealthResource, summary="更新特定心理健康資源")
def patch_mental_health_resource(
        id: str, resource_in: schemas.MentalHealthResourcePatch, db: Session = Depends(get_db)
):
    """
    更新心理健康資源 (部分欄位)
    """
    db_resource = crud.get_by_id(db, models.MentalHealthResource, id)
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Mental Health Resource not found")
    return crud.update(db, db_obj=db_resource, obj_in=resource_in)
