from fastapi import FastAPI
from app.core.config import settings
from app.routers import user  

app = FastAPI()

app.include_router(user.router)

@app.get("/")
def read_root():
    return {"message": "Hello, world", "env_loaded": settings.JWT_SECRET}
