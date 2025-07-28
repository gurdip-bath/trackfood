from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import user, ping
from app.core.database import Base, engine

# Create FastAPI app
app = FastAPI()

# CORS middleware - MUST be added before route includes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers AFTER CORS middleware
app.include_router(user.router, prefix="/api")
app.include_router(ping.router, prefix="/api")

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Hello, world", "env_loaded": bool(settings.DATABASE_URL)}