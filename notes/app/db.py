# app/db.py
from sqlmodel import SQLModel, create_engine, Session

sqlite_file_name = "notes.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# check_same_thread=False helps SQLite work across threads (useful for uvicorn dev)
engine = create_engine(sqlite_url, echo=False, connect_args={"check_same_thread": False})

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
