from functools import wraps
from typing import Type

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, select


async def validate_resource_exists(id: int, model: Type[SQLModel], db: AsyncSession):
    result = await db.execute(select(model).filter(model.id == id))
    resource = result.scalars().first()
    if not resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{model.__name__} not found")
    return resource


def validate_resource(model: Type[SQLModel]):
    def decorator(func):
        @wraps(func)
        async def wrapper(course_id: int, *args, db: AsyncSession, **kwargs):
            resource = await validate_resource_exists(course_id, model, db)
            return await func(course_id, resource, *args, db=db, **kwargs)

        return wrapper

    return decorator
