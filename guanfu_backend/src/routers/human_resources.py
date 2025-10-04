from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from .. import crud, models, schemas
from ..database import get_db
from ..schemas import GeneralStatusEnum, HumanResourceRoleStatusEnum, HumanResourceRoleTypeEnum

router = APIRouter(
    prefix="/human_resources",
    tags=["人力需求（Human Resources）"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=schemas.HumanResourceCollection, summary="取得人力需求清單")
def list_human_resources(
        status: Optional[GeneralStatusEnum] = Query(None),
        role_status: Optional[HumanResourceRoleStatusEnum] = Query(None),
        role_type: Optional[HumanResourceRoleTypeEnum] = Query(None),
        limit: int = Query(20, ge=1, le=200),
        offset: int = Query(0, ge=0),
        db: Session = Depends(get_db)
):
    """
    取得人力需求清單 (分頁)
    """
    filters = {
        "status": status,
        "role_status": role_status,
        "role_type": role_type,
    }
    resources = crud.get_multi(db, models.HumanResource, skip=offset, limit=limit, **filters)
    total = crud.count(db, models.HumanResource, **filters)
    return {"member": resources, "totalItems": total, "limit": limit, "offset": offset}


@router.post("/", response_model=schemas.HumanResource, status_code=201, summary="建立人力需求")
def create_human_resource(
        resource_in: schemas.HumanResourceCreate, db: Session = Depends(get_db)
):
    """
    建立人力需求/角色
    """
    return crud.create(db, models.HumanResource, obj_in=resource_in)


@router.get("/{id}", response_model=schemas.HumanResource, summary="取得特定人力需求")
def get_human_resource(id: str, db: Session = Depends(get_db)):
    """
    取得單一人力需求/角色
    """
    db_resource = crud.get_by_id(db, models.HumanResource, id)
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Human Resource not found")
    return db_resource


@router.patch("/{id}", response_model=schemas.HumanResource, summary="更新特定人力需求")
def patch_human_resource(
        id: str, resource_in: schemas.HumanResourcePatch, db: Session = Depends(get_db)
):
    """
    更新人力需求/角色 (部分欄位)
    """
    db_resource = crud.get_by_id(db, models.HumanResource, id)
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Human Resource not found")
    return crud.update(db, db_obj=db_resource, obj_in=resource_in)
