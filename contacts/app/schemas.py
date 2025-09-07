# app/schemas.py
from typing import Optional
from sqlmodel import SQLModel
from pydantic import EmailStr

class UserCreate(SQLModel):
    username: str
    password: str

class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"

class ContactCreate(SQLModel):
    name: str
    email: EmailStr
    phone: str

class ContactRead(ContactCreate):
    id: int
    user_id: int

class ContactUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
