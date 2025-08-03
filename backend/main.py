from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import user, ping
from app.core.database import create_tables

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers AFTER CORS middleware
app.include_router(user.router, prefix="/api")
app.include_router(ping.router, prefix="/api")

create_tables()  

@app.get("/")
def read_root():
    return {"message": "Hello, world", "env_loaded": bool(settings.DATABASE_URL)}