from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserRead
from app.services.user import create_user
from app.core.database import get_db
from app.utils.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=UserRead)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user_in)

@router.get("/me", response_model=UserRead)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user 

@router.get("/dashboard")
def dashboard(current_user: User = Depends(get_current_user)):
    return {"msg": f"Welcome {current_user.email}"}

