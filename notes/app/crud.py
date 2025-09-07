# app/crud.py
from sqlmodel import select
from app.models import Note
from .utils import dump_notes_to_file

def create_note_in_db(session, title: str, content: str):
    note = Note(title=title, content=content)
    session.add(note)
    session.commit()
    session.refresh(note)
    # update JSON backup after change
    dump_notes_to_file(session)
    return note

def list_notes(session):
    statement = select(Note)
    return session.exec(statement).all()

def get_note(session, note_id: int):
    return session.get(Note, note_id)

def delete_note(session, note_id: int):
    note = session.get(Note, note_id)
    if not note:
        return None
    session.delete(note)
    session.commit()
    # update JSON backup after change
    dump_notes_to_file(session)
    return note
