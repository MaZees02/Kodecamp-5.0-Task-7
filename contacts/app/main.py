# app/main.py
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
import logging

from app.db import init_db, get_session
from .models import Contact
from .schemas import UserCreate, Token, ContactCreate, ContactRead, ContactUpdate
from .auth import register_user, authenticate_user, create_access_token, get_current_user
import app.crud as crud

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

app = FastAPI(title="Contact Manager API")

# CORS: allow all origins for ease of dev; in production set specific origins.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # <-- change to a whitelist in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

# Middleware: log IP address of every request
@app.middleware("http")
async def log_ip_middleware(request: Request, call_next):
    # Try X-Forwarded-For first (if behind proxy), fallback to request.client
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        ip = forwarded.split(",")[0].strip()
    else:
        client = request.client
        ip = client.host if client else "unknown"
    logging.info(f"Request from IP={ip} Method={request.method} Path={request.url.path}")
    response = await call_next(request)
    return response

# AUTH endpoints
@app.post("/auth/register", response_model=Token, status_code=201)
def api_register(payload: UserCreate, session: Session = Depends(get_session)):
    user = register_user(session, payload.username, payload.password)
    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/auth/login", response_model=Token)
def api_login(payload: UserCreate, session: Session = Depends(get_session)):
    user = authenticate_user(session, payload.username, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# CONTACT endpoints
@app.post("/contacts/", response_model=ContactRead, status_code=201)
def create_contact(payload: ContactCreate, session: Session = Depends(get_session), user = Depends(get_current_user)):
    contact = crud.create_contact(session, user.id, payload.name, payload.email, payload.phone)
    return contact

@app.get("/contacts/", response_model=list[ContactRead])
def list_contacts(session: Session = Depends(get_session), user = Depends(get_current_user)):
    return crud.list_contacts(session, user.id)

@app.put("/contacts/{contact_id}", response_model=ContactRead)
def update_contact(contact_id: int, payload: ContactUpdate, session: Session = Depends(get_session), user = Depends(get_current_user)):
    contact = crud.get_contact(session, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    if contact.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed to modify this contact")
    contact = crud.update_contact(session, contact, payload.name, payload.email, payload.phone)
    return contact

@app.delete("/contacts/{contact_id}", status_code=204)
def delete_contact(contact_id: int, session: Session = Depends(get_session), user = Depends(get_current_user)):
    contact = crud.get_contact(session, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    if contact.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed to delete this contact")
    crud.delete_contact(session, contact)
    return None
