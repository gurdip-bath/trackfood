from fastapi import APIRouter, Depends
from app.dependencies.supabase_auth import get_current_user
from app.schemas.user import UserRead        
router = APIRouter()

@router.get("/ping", response_model=dict)
def ping(current_user: UserRead = Depends(get_current_user)):
    return {"msg": "pong", "user_email": current_user.email}
