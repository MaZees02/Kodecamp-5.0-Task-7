from fastapi import Depends
from .database import get_session
from .auth import get_current_user

SessionDep = get_session
CurrentUserDep = get_current_user