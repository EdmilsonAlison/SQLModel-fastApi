import logging
from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from sqlmodel.sql.expression import Select, SelectOfScalar

from core.deps import get_db
from models.course import CourseModel
from util.validate_sql import validate_resource

SelectOfScalar.inherit_cache = True
Select.inherit_cache = True

router = APIRouter()


@router.post('/', response_model=CourseModel, status_code=status.HTTP_201_CREATED)
def create_course(course: CourseModel, db: AsyncSession = Depends(get_db)):
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


@router.get('/', response_model=List[CourseModel], status_code=status.HTTP_200_OK)
async def get_courses(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CourseModel))
    courses = result.scalars().all()
    logging.info(courses)
    return courses


@router.get('/{course_id}', response_model=CourseModel, status_code=status.HTTP_200_OK)
@validate_resource(CourseModel)
def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    course = db.get(CourseModel, course_id)
    return course


@router.put('/{course_id}', response_model=CourseModel, status_code=status.HTTP_200_OK)
@validate_resource(CourseModel)
async def update_course(course: CourseModel, existing_course: CourseModel, db: AsyncSession = Depends(get_db)):
    for key, value in course.dict().items():
        setattr(existing_course, key, value)
    db.add(existing_course)
    await db.commit()
    await db.refresh(existing_course)
    return existing_course


@router.delete('/{course_id}', status_code=status.HTTP_204_NO_CONTENT)
@validate_resource(CourseModel)
async def delete_course(existing_course: CourseModel, db: AsyncSession = Depends(get_db)):
    await db.delete(existing_course)
    await db.commit()
    return None
