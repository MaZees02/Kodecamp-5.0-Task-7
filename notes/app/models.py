# app/models.py
from typing import Optional
from sqlmodel import SQLModel, Field
import datetime

class NoteBase(SQLModel):
    title: str
    content: str

class Note(NoteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

# Schema used for creating (no id / created_at required)
class NoteCreate(NoteBase):
    pass
