from fastapi import FastAPI
from app.core.config import settings
from app.routers import user  
from app.core.database import Base, engine

app = FastAPI()

app.include_router(user.router)

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Hello, world", "env_loaded": settings.JWT_SECRET}
