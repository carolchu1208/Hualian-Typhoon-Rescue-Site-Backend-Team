from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from .. import crud, models, schemas
from ..database import get_db
from ..enum_serializer import HumanResourceRoleStatusEnum, HumanResourceRoleTypeEnum, HumanResourceStatusEnum
from ..pin_related import generate_pin

router = APIRouter(
    prefix="/human_resources",
    tags=["人力需求（Human Resources）"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=schemas.HumanResourceCollection, summary="取得人力需求清單")
def list_human_resources(
        status: Optional[HumanResourceStatusEnum] = Query(None),
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


@router.post("/", response_model=schemas.HumanResourceWithPin, status_code=201, summary="建立人力需求")
def create_human_resource(
        resource_in: schemas.HumanResourceCreate, db: Session = Depends(get_db)
):
    """
    建立人力需求/角色
    """
    if resource_in.headcount_got > resource_in.headcount_need:
        raise HTTPException(status_code=400, detail="headcount_got must be less than or equal to headcount_need.")
    return crud.create_with_input(db, models.HumanResource, obj_in=resource_in, valid_pin=generate_pin())


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
    if db_resource.valid_pin and db_resource.valid_pin != resource_in.valid_pin:
        raise HTTPException(status_code=400, detail="The PIN you entered is incorrect.")
    # validate num
    if resource_in.headcount_need is not None or resource_in.headcount_got is not None:
        if resource_in.headcount_need == resource_in.headcount_got:
            raise HTTPException(status_code=400, detail="headcount_need and headcount_got are locked because their values are equal; updates are not allowed.")
        headcount_need = resource_in.headcount_need if resource_in.headcount_need is not None else db_resource.headcount_need
        headcount_got = resource_in.headcount_got if resource_in.headcount_got is not None else db_resource.headcount_got
        if headcount_got > headcount_need:
            raise HTTPException(status_code=400, detail="headcount_got must be less than or equal to headcount_need.")
    return crud.update(db, db_obj=db_resource, obj_in=resource_in)
