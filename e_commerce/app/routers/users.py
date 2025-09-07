from fastapi import APIRouter, Depends
from app.auth import login

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/login")
async def user_login(token=Depends(login)):
    return token