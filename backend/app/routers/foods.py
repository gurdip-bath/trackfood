from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.nutrition import Food
from app.schemas.nutrition import FoodCreate, FoodRead

router = APIRouter(prefix="/foods", tags=["Foods"])

@router.get("/", response_model=List[FoodRead])
def get_foods(
    search: Optional[str] = Query(None, description="Search foods by name"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: Session = Depends(get_db)
):
    """Get all foods with optional search and pagination."""
    query = db.query(Food)
    
    if search:
        query = query.filter(Food.name.ilike(f"%{search}%"))
    
    foods = query.order_by(Food.name).offset(skip).limit(limit).all()
    return foods

@router.get("/{food_id}", response_model=FoodRead)
def get_food(food_id: int, db: Session = Depends(get_db)):
    """Get a single food by ID."""
    food = db.query(Food).filter(Food.id == food_id).first()
    
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    
    return food

@router.post("/", response_model=FoodRead, status_code=201)
def create_food(food_data: FoodCreate, db: Session = Depends(get_db)):
    """Create a new food item."""
    # Check for duplicate names
    existing = db.query(Food).filter(Food.name == food_data.name).first()
    if existing:
        raise HTTPException(status_code=409, detail="Food already exists")
    
    new_food = Food(**food_data.dict())
    db.add(new_food)
    db.commit()
    db.refresh(new_food)
    
    return new_food

@router.put("/{food_id}", response_model=FoodRead)
def update_food(
    food_id: int, 
    food_data: FoodCreate, 
    db: Session = Depends(get_db)
):
    """Update an existing food item."""
    food = db.query(Food).filter(Food.id == food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    
    # Check for name conflicts with other foods
    if food_data.name != food.name:
        existing = db.query(Food).filter(
            Food.name == food_data.name,
            Food.id != food_id
        ).first()
        if existing:
            raise HTTPException(status_code=409, detail="Name already taken")
    
    # Update all fields
    for field, value in food_data.dict().items():
        setattr(food, field, value)
    
    db.commit()
    db.refresh(food)
    return food

@router.delete("/{food_id}")
def delete_food(food_id: int, db: Session = Depends(get_db)):
    """Delete a food item."""
    food = db.query(Food).filter(Food.id == food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    
    # Check if food is used in any meal entries
    from app.models.nutrition import FoodEntry
    has_entries = db.query(FoodEntry).filter(FoodEntry.food_id == food_id).first()
    if has_entries:
        raise HTTPException(
            status_code=409, 
            detail="Cannot delete food - it's used in meals"
        )
    
    db.delete(food)
    db.commit()
    return {"message": f"Food '{food.name}' deleted successfully"}