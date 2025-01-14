from typing import Optional

from sqlmodel import SQLModel, Field


class CourseModel(SQLModel, table=True):
    __tablename__: str = 'courses'

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    classes: int
    hours: int

