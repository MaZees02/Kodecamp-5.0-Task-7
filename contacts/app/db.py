# app/db.py
from sqlmodel import SQLModel, create_engine, Session

sqlite_file_name = "contacts.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# check_same_thread False helps SQLite work with uvicorn
engine = create_engine(sqlite_url, echo=False, connect_args={"check_same_thread": False})

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    """
    Dependency to get a DB session (yielded).
    Use: session: Session = Depends(get_session)
    """
    with Session(engine) as session:
        yield session
