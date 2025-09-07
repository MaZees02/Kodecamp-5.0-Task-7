# app/crud.py
from sqlmodel import Session, select
from .models import JobApplication
from typing import List

# Acceptable statuses:
STATUSES = {"pending", "interviewing", "rejected", "accepted", "offer"}

def create_application(session: Session, user_id: int, company: str, position: str, date_applied, status: str = "pending") -> JobApplication:
    if status not in STATUSES:
        raise ValueError(f"Invalid status. Allowed: {', '.join(sorted(STATUSES))}")
    app = JobApplication(company=company, position=position, date_applied=date_applied, status=status, user_id=user_id)
    session.add(app)
    session.commit()
    session.refresh(app)
    return app

def list_applications(session: Session, user_id: int) -> List[JobApplication]:
    statement = select(JobApplication).where(JobApplication.user_id == user_id)
    return session.exec(statement).all()

def search_applications_by_status(session: Session, user_id: int, status: str) -> List[JobApplication]:
    if status not in STATUSES:
        raise ValueError(f"Invalid status. Allowed: {', '.join(sorted(STATUSES))}")
    statement = select(JobApplication).where(JobApplication.user_id == user_id, JobApplication.status == status)
    return session.exec(statement).all()
