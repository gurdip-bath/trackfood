from pydantic import BaseModel

# Input for login
class LoginRequest(BaseModel):
    email: str
    password: str

# Output for login response

class LogingResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"