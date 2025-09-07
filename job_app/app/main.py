# app/main.py
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlmodel import Session
from app.db import init_db, get_session
from .auth import register_user, authenticate_user, create_token_for_user, get_current_user
from .crud import create_application, list_applications, search_applications_by_status, STATUSES
from .models import JobApplication, User
from pydantic import BaseModel
import datetime

app = FastAPI(title="Job Application Tracker")

# Create DB tables at startup
@app.on_event("startup")
def on_startup():
    init_db()

# Middleware: reject requests missing User-Agent header
@app.middleware("http")
async def require_user_agent(request: Request, call_next):
    if not request.headers.get("user-agent"):
        return JSONResponse(status_code=400, content={"detail": "User-Agent header required"})
    return await call_next(request)

# Request/response models
class RegisterIn(BaseModel):
    username: str
    password: str

class LoginIn(BaseModel):
    username: str
    password: str

class ApplicationCreate(BaseModel):
    company: str
    position: str
    status: str = "pending"
    date_applied: datetime.date

# AUTH endpoints
@app.post("/auth/register")
def api_register(data: RegisterIn, session: Session = Depends(get_session)):
    return register_user(session, data.username, data.password)

@app.post("/auth/login")
def api_login(data: LoginIn, session: Session = Depends(get_session)):
    user = authenticate_user(session, data.username, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_token_for_user(session, user)
    return {"token": token}

# APPLICATION endpoints
@app.post("/applications/", response_model=JobApplication)
def api_create_application(payload: ApplicationCreate, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    try:
        app_obj = create_application(session, user.id, payload.company, payload.position, payload.date_applied, payload.status)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return app_obj

@app.get("/applications/")
def api_list_applications(user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    return list_applications(session, user.id)

@app.get("/applications/search")
def api_search(status: str, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    try:
        return search_applications_by_status(session, user.id, status)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
