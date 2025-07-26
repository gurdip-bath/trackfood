from fastapi import FastAPI
from app.core.config import settings
from app.routers import user  
from app.core.database import Base, engine
from app.routers import ping  # Import the ping router

app = FastAPI()

app.include_router(user.router)
app.include_router(ping.router)  # Include the ping router

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Hello, world", "env_loaded": settings.JWT_SECRET}
