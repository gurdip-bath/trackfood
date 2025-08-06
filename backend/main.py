from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import user, ping
from app.routers.foods import router as foods_router
from app.core.database import create_tables
from app.routers.meals import router as meals_router

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
app.include_router(foods_router, prefix="/api")
app.include_router(meals_router, prefix="/api")

create_tables()  

@app.get("/")
def read_root():
    return {"message": "Hello, world", "env_loaded": bool(settings.DATABASE_URL)}