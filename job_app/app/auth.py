# app/auth.py
from fastapi import HTTPException, status, Header, Depends
from sqlmodel import Session, select
from passlib.context import CryptContext
from uuid import uuid4
from .models import User, Token
from .db import get_session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def register_user(session: Session, username: str, password: str) -> User:
    existing = session.exec(select(User).where(User.username == username)).first()
    if existing:
        raise HTTPException(status_code=400, detail="username already exists")
    user = User(username=username, hashed_password=hash_password(password))
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def authenticate_user(session: Session, username: str, password: str) -> User | None:
    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def create_token_for_user(session: Session, user: User) -> str:
    token_str = str(uuid4())
    token = Token(token=token_str, user_id=user.id)
    session.add(token)
    session.commit()
    session.refresh(token)
    return token_str

# Dependency to get the current user from Authorization: Bearer <token>
def get_current_user(authorization: str = Header(None), session: Session = Depends(get_session)) -> User:
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header required")
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization format")
    token_str = parts[1]
    token_obj = session.exec(select(Token).where(Token.token == token_str)).first()
    if not token_obj:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = session.exec(select(User).where(User.id == token_obj.user_id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
