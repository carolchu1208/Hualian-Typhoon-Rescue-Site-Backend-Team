from sqlalchemy.orm import Session
from typing import List, Optional, Type, TypeVar
from . import models
from pydantic import BaseModel

ModelType = TypeVar("ModelType", bound=models.Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


def get_by_id(db: Session, model: Type[ModelType], id: str) -> Optional[ModelType]:
    return db.query(model).filter(model.id == id).first()


def get_multi(db: Session, model: Type[ModelType], skip: int = 0, limit: int = 100, **filters) -> List[Type[ModelType]]:
    query = db.query(model)
    if filters:
        query = query.filter_by(**{k: v for k, v in filters.items() if v is not None})
    return query.offset(skip).limit(limit).all()


def count(db: Session, model: Type[ModelType], **filters) -> int:
    query = db.query(model)
    if filters:
        query = query.filter_by(**{k: v for k, v in filters.items() if v is not None})
    return query.count()


def create(db: Session, model: Type[ModelType], obj_in: CreateSchemaType) -> ModelType:
    db_obj = model(**obj_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(db: Session, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
    update_data = obj_in.model_dump(exclude_unset=True)
    for field in update_data:
        setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
