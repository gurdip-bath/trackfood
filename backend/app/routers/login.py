from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.login import LoginRequest, LoginResponse
from app.services.login import authenticate_user
from app.dependencies import get_db

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
def login_user(login_data: LoginRequest, db: Session = Depends(get_db)):
    token = authenticate_user(db, login_data)
    return {"access_token": token, "token_type": "bearer"}
