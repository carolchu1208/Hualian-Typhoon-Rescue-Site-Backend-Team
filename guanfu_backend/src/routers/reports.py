from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from .. import crud, models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/reports",
    tags=["回報事件（Reports）"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=schemas.ReportCollection, summary="取得回報事件清單")
def list_reports(
        status: Optional[bool] = Query(None),
        limit: int = Query(50, ge=1, le=500),
        offset: int = Query(0, ge=0),
        db: Session = Depends(get_db)
):
    """
    取得回報事件清單 (分頁)
    """
    filters = {"status": status}
    reports = crud.get_multi(db, models.Report, skip=offset, limit=limit, **filters)
    total = crud.count(db, models.Report, **filters)
    return {"member": reports, "totalItems": total, "limit": limit, "offset": offset}


@router.post("/", response_model=schemas.Report, status_code=201, summary="建立回報事件")
def create_report(
        report_in: schemas.ReportCreate, db: Session = Depends(get_db)
):
    """
    建立回報事件
    """
    return crud.create(db, models.Report, obj_in=report_in)


@router.get("/{id}", response_model=schemas.Report, summary="取得特定回報事件")
def get_report(id: str, db: Session = Depends(get_db)):
    """
    取得單一回報事件
    """
    db_report = crud.get_by_id(db, models.Report, id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return db_report


@router.patch("/{id}", response_model=schemas.Report, summary="更新特定回報事件")
def patch_report(
        id: str, report_in: schemas.ReportPatch, db: Session = Depends(get_db)
):
    """
    更新回報事件 (部分欄位)
    """
    db_report = crud.get_by_id(db, models.Report, id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return crud.update(db, db_obj=db_report, obj_in=report_in)
