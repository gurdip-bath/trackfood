from sqlalchemy.orm import Session
from app.schemas.login import LoginRequest
from app.models.user import User
from passlib.context import CryptContext
from app.utils.auth import create_access_token
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def authenticate_user(db: Session, login_data: LoginRequest):
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user or not pwd_context.verify(login_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return create_access_token(data={"sub": user.email})
