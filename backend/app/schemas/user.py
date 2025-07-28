from pydantic import BaseModel, EmailStr
from typing import Optional

# Input for registration
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Output to client (no password) - for database users
class UserRead(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

    class Config:
        orm_mode = True

# Output for Supabase JWT users (no database id)
class UserJWT(BaseModel):
    email: EmailStr
    sub: Optional[str] = None  # Supabase user ID