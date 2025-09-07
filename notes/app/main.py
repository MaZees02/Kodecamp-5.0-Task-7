# app/main.py
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
from typing import List
import logging
import threading

from app.db import init_db, get_session
from .models import Note, NoteCreate
import app.crud as crud  # relative import for clarity

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

app = FastAPI(title="Notes API (DB + JSON backup)")

# CORS: allow the two specified origins
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:5500"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DB & middleware state on startup
@app.on_event("startup")
def on_startup():
    init_db()
    # state used by request-counter middleware
    app.state.request_count = 0
    app.state.request_count_lock = threading.Lock()

# Middleware: count total requests and log them
@app.middleware("http")
async def request_counter_middleware(request: Request, call_next):
    # increment counter safely
    with app.state.request_count_lock:
        app.state.request_count += 1
        current_count = app.state.request_count

    logging.info(f"[Requests={current_count}] {request.method} {request.url.path}")
    # proceed to route handler
    response = await call_next(request)
    # expose the counter value to clients optionally
    response.headers["X-Total-Requests"] = str(current_count)
    return response

# ROUTES

@app.post("/notes/", response_model=Note, status_code=201)
def create_note(payload: NoteCreate, session: Session = Depends(get_session)):
    note = crud.create_note_in_db(session, payload.title, payload.content)
    return note

@app.get("/notes/", response_model=List[Note])
def read_notes(session: Session = Depends(get_session)):
    return crud.list_notes(session)

@app.get("/notes/{note_id}", response_model=Note)
def read_note(note_id: int, session: Session = Depends(get_session)):
    note = crud.get_note(session, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int, session: Session = Depends(get_session)):
    note = crud.delete_note(session, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    # 204 No Content => return nothing
    return None
