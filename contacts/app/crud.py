# app/crud.py
from sqlmodel import select
from .models import Contact

def create_contact(session, user_id: int, name: str, email: str, phone: str):
    c = Contact(name=name, email=email, phone=phone, user_id=user_id)
    session.add(c)
    session.commit()
    session.refresh(c)
    return c

def list_contacts(session, user_id: int):
    stmt = select(Contact).where(Contact.user_id == user_id)
    return session.exec(stmt).all()

def get_contact(session, contact_id: int):
    return session.get(Contact, contact_id)

def update_contact(session, contact: Contact, name: str | None = None, email: str | None = None, phone: str | None = None):
    updated = False
    if name is not None:
        contact.name = name; updated = True
    if email is not None:
        contact.email = email; updated = True
    if phone is not None:
        contact.phone = phone; updated = True
    if updated:
        session.add(contact)
        session.commit()
        session.refresh(contact)
    return contact

def delete_contact(session, contact: Contact):
    session.delete(contact)
    session.commit()
    return
