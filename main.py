from fastapi import FastAPI
from app.core.config import settings

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, world", "env_loaded": settings.JWT_SECRET}
