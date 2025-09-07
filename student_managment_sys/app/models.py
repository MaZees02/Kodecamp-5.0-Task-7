from __future__ import annotations
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
#from sqlmodel import SQLModel, Field, create_engine, Session, select


class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: int
    email: str = Field(index=True, unique=True)

    grades: List["Grade"] = Relationship(
        back_populates="student",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class Grade(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    subject: str
    score: float

    student_id: int = Field(foreign_key="student.id")
    student: Optional[Student] = Relationship(back_populates="grades")
