from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext

from .config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, USERS_FILE
from .schemas import Token


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# ---------- user store helpers ----------

def _ensure_users_file() -> None:
    p = Path(USERS_FILE)
    if not p.exists():
        p.write_text("[]", encoding="utf-8")


def _load_users():
    _ensure_users_file()
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _get_user(username: str) -> Optional[dict]:
    for u in _load_users():
        if u.get("username") == username:
            return u
    return None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    to_encode = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ---------- FastAPI dependencies ----------

def authenticate_user(username: str, password: str) -> bool:
    user = _get_user(username)
    if not user:
        return False
    return verify_password(password, user.get("hashed_password", ""))


async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    if not authenticate_user(form_data.username, form_data.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(subject=form_data.username)
    return Token(access_token=token)


def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")  # type: ignore
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    if not _get_user(username):
        raise credentials_exception
    return username  # return username as the current user identity
