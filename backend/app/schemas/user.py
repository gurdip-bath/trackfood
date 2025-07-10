from pydantic import BaseModel, EmailStr

# Input for registration
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Output to client (no password)
class UserRead(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

    class Config:
        orm_mode = True  # ← needed to convert SQLAlchemy models to Pydantic
