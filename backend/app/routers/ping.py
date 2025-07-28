from fastapi import APIRouter, Depends
from app.dependencies.supabase_auth import get_current_user
from app.schemas.user import UserJWT

# Remove prefix here since it's added in main.py
router = APIRouter(tags=["Ping"])

@router.get("/ping")
async def ping(current_user: UserJWT = Depends(get_current_user)):
    return {"message": f"Welcome, {current_user.email}", "user_id": current_user.sub}