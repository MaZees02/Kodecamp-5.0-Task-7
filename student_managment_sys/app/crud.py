from typing import List, Optional
from fastapi import HTTPException, status
from sqlmodel import select
from sqlmodel import Session
#from .models import Student, Grade
from app.models import Student, Grade


def list_students(session: Session) -> List[Student]:
    # Eager-load grades to avoid lazy-loading issues
    statement = select(Student).order_by(Student.id)
    students = session.exec(statement).all()
    # Access .grades once to ensure they load while session is open
    for s in students:
        _ = s.grades
    return students


def get_student(session: Session, student_id: int) -> Student:
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    _ = student.grades
    return student


def create_student(session: Session, name: str, age: int, email: str, grades_payload: Optional[List[dict]]):
    # Unique email check
    existing = session.exec(select(Student).where(Student.email == email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    student = Student(name=name, age=age, email=email)
    session.add(student)
    session.commit()
    session.refresh(student)

    if grades_payload:
        for g in grades_payload:
            session.add(Grade(subject=g["subject"], score=g["score"], student_id=student.id))
        session.commit()

    _ = student.grades
    return student


def update_student(session: Session, student_id: int, data: dict) -> Student:
    student = get_student(session, student_id)

    if (email := data.get("email")) and email != student.email:
        if session.exec(select(Student).where(Student.email == email)).first():
            raise HTTPException(status_code=400, detail="Email already exists")
        student.email = email

    if (name := data.get("name")) is not None:
        student.name = name
    if (age := data.get("age")) is not None:
        student.age = age

    # Replace grades if provided
    if "grades" in data and data["grades"] is not None:
        # Delete old
        for g in list(student.grades):
            session.delete(g)
        session.commit()
        # Add new
        for g in data["grades"]:
            session.add(Grade(subject=g["subject"], score=g["score"], student_id=student.id))
        session.commit()

    session.add(student)
    session.commit()
    session.refresh(student)
    _ = student.grades
    return student


def delete_student(session: Session, student_id: int) -> None:
    student = get_student(session, student_id)
    session.delete(student)
    session.commit()