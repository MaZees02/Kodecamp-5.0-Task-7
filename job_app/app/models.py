# app/models.py
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    hashed_password: str

    tokens: List["Token"] = Relationship(back_populates="user")
    applications: List["JobApplication"] = Relationship(back_populates="user")

class Token(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    token: str
    user_id: int = Field(foreign_key="user.id")

    user: Optional[User] = Relationship(back_populates="tokens")

class JobApplication(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    company: str
    position: str
    status: str = Field(default="pending")
    date_applied: datetime.date

    user_id: int = Field(foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="applications")
