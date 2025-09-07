from typing import List
from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware

from app.config import ALLOWED_ORIGINS
from .database import init_db, get_session
#from .middleware import RequestLoggerMiddleware
from app.middleware import RequestLoggerMiddleware
from .schemas import StudentCreate, StudentRead, StudentUpdate, GradeRead
from .auth import login_for_access_token, get_current_user
from . import crud
from sqlmodel import Session

app = FastAPI(title="Student Management API")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging
app.add_middleware(RequestLoggerMiddleware)

@app.on_event("startup")
def on_startup():
    init_db()

# ---------- AUTH ----------
@app.post("/auth/login")
async def login(token=Depends(login_for_access_token)):
    return token

# ---------- STUDENTS ----------
@app.get("/students/", response_model=List[StudentRead])
def list_students(session: Session = Depends(get_session)):
    students = crud.list_students(session)
    return [
        StudentRead(
            id=s.id, name=s.name, age=s.age, email=s.email,
            grades=[GradeRead(id=g.id, subject=g.subject, score=g.score) for g in s.grades],
        ) for s in students
    ]

@app.post("/students/", response_model=StudentRead, status_code=status.HTTP_201_CREATED)
def create_student(payload: StudentCreate, session: Session = Depends(get_session), current_user: str = Depends(get_current_user)):
    s = crud.create_student(session, payload.name, payload.age, payload.email,
                            [g.model_dump() for g in (payload.grades or [])])
    return StudentRead(
        id=s.id, name=s.name, age=s.age, email=s.email,
        grades=[GradeRead(id=g.id, subject=g.subject, score=g.score) for g in s.grades],
    )