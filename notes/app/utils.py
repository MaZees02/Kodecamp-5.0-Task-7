# app/utils.py
import json
import threading
from sqlmodel import select
from app.models import Note

_file_lock = threading.Lock()

def dump_notes_to_file(session, path: str = "notes.json"):
    """
    Write all notes to notes.json (overwrites).
    Uses a simple lock to reduce concurrency issues.
    """
    with _file_lock:
        notes = session.exec(select(Note)).all()
        out = []
        for n in notes:
            out.append({
                "id": n.id,
                "title": n.title,
                "content": n.content,
                "created_at": n.created_at.isoformat() if n.created_at else None
            })
        with open(path, "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2, ensure_ascii=False)
