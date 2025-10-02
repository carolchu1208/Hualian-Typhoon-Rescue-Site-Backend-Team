from typing import List
import uuid

from pydantic.v1 import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.todos import schemas, models, crud


def get_todo_by_user(db: Session, user_id: UUID4) -> models.Todo | List:
    if user_id is None:
        raise ValueError("User not found")

    todo = crud.get_todo(db, user_id)
    return todo


async def create_todo_by_user(db: Session, user_id: UUID4, todo_data: schemas.Todo) -> models.Todo | List:
    if user_id is None:
        raise ValueError("User not found")
    qsTodo = models.Todo(
        user_id=user_id,  # fk User

        title=todo_data.title,
        description=todo_data.description,
        sort=todo_data.sort,
    )
    return crud.create_todo(db, qsTodo)


async def update_todo_by_user(db: Session, user_id: UUID4, todo_datas: schemas.TodoUpdate) -> models.Todo | List:
    if user_id is None:
        raise ValueError("User not found")
    return crud.update_todos(db, todo_datas)


async def delete_todo_by_user(db: Session, user_id: UUID4, todo_id: UUID4) -> models.Todo | List:
    if user_id is None:
        raise ValueError("User not found")
    return crud.delete_todo(db, user_id, todo_id)
