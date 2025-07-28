# app/routers/dashboard.py
from fastapi import APIRouter, Depends
from app.dependencies.supabase_auth import get_current_user
from app.schemas.user import UserRead

router = APIRouter()

@router.get("/ping", response_model=UserRead)
async def ping(current_user: UserRead = Depends(get_current_user)):
    return current_user
