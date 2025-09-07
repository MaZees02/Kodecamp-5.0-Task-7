from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


class GradeCreate(BaseModel):
    subject: str
    score: float


class GradeRead(BaseModel):
    id: int
    subject: str
    score: float


class StudentCreate(BaseModel):
    name: str
    age: int = Field(ge=0, le=150)
    email: EmailStr
    grades: Optional[List[GradeCreate]] = None


class StudentRead(BaseModel):
    id: int
    name: str
    age: int
    email: EmailStr
    grades: List[GradeRead] = []


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = Field(default=None, ge=0, le=150)
    email: Optional[EmailStr] = None
    # If provided, we’ll REPLACE existing grades with this list
    grades: Optional[List[GradeCreate]] = None


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"