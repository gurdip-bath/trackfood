from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.nutrition import FoodEntry, Food, Meal
from app.schemas.nutrition import FoodEntryCreate, FoodEntryRead
from app.dependencies.supabase_auth import get_current_user
from app.schemas.user import UserJWT

router = APIRouter(prefix="/food-entries", tags=["Food Entries"])

def calculate_nutrition(food: Food, quantity_grams: float) -> dict:
    """
    Calculate nutrition totals for a specific quantity.
    
    WHY separate function: Reusable logic for create/update operations
    WHY simple math: Food table stores per-100g, we scale to actual quantity
    """
    multiplier = quantity_grams / 100.0 
    
    return {
        "total_calories": food.calories_per_100g * multiplier,
        "total_protein": food.protein_per_100g * multiplier,
        "total_carbs": food.carbs_per_100g * multiplier,
        "total_fat": food.fat_per_100g * multiplier
    }

@router.get("/", response_model=List[FoodEntryRead])
def get_food_entries(
    meal_id: Optional[int] = Query(None, description="Filter by meal ID"),
    food_id: Optional[int] = Query(None, description="Filter by food ID"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    current_user: UserJWT = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's food entries with filtering options.
    
    WHY join with Meal: Security - ensure user can only see their own entries
    WHY include Food data: Frontend needs food name/details for display
    """
    # Security: Join with Meal to ensure user ownership
    query = db.query(FoodEntry)\
        .join(Meal)\
        .filter(Meal.user_id == current_user.sub)
    
    if meal_id:
        query = query.filter(FoodEntry.meal_id == meal_id)
    
    if food_id:
        query = query.filter(FoodEntry.food_id == food_id)
    
    query = query.order_by(Meal.date.desc(), FoodEntry.id.desc())
    
    entries = query.offset(skip).limit(limit).all()
    return entries

@router.get("/{entry_id}", response_model=FoodEntryRead)
def get_food_entry(
    entry_id: int,
    current_user: UserJWT = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific food entry by ID with ownership check.
    """
    entry = db.query(FoodEntry)\
        .join(Meal)\
        .filter(
            FoodEntry.id == entry_id,
            Meal.user_id == current_user.sub  
        ).first()
    
    if not entry:
        raise HTTPException(status_code=404, detail="Food entry not found")
    
    return entry

@router.post("/", response_model=FoodEntryRead, status_code=201)
def create_food_entry(
    entry_data: FoodEntryCreate,
    current_user: UserJWT = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new food entry with automatic nutrition calculation.
    
    WHY validate meal ownership: Security - can't add entries to others' meals
    WHY validate food exists: Data integrity - can't reference non-existent food
    WHY auto-calculate nutrition: User shouldn't do math, system should
    """
    meal = db.query(Meal).filter(
        Meal.id == entry_data.meal_id,
        Meal.user_id == current_user.sub  
    ).first()
    
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found or not accessible")
    
    food = db.query(Food).filter(Food.id == entry_data.food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    
    nutrition = calculate_nutrition(food, entry_data.quantity_grams)
    
    new_entry = FoodEntry(
        meal_id=entry_data.meal_id,
        food_id=entry_data.food_id,
        quantity_grams=entry_data.quantity_grams,
        **nutrition  
    )
    
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    
    return new_entry

@router.put("/{entry_id}", response_model=FoodEntryRead)
def update_food_entry(
    entry_id: int,
    entry_data: FoodEntryCreate,
    current_user: UserJWT = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update food entry with recalculated nutrition totals.
    
    WHY recalculate on update: Quantity or food might change
    WHY validate new meal/food: User might change references
    """
    entry = db.query(FoodEntry)\
        .join(Meal)\
        .filter(
            FoodEntry.id == entry_id,
            Meal.user_id == current_user.sub
        ).first()
    
    if not entry:
        raise HTTPException(status_code=404, detail="Food entry not found")
    
    if entry_data.meal_id != entry.meal_id:
        meal = db.query(Meal).filter(
            Meal.id == entry_data.meal_id,
            Meal.user_id == current_user.sub
        ).first()
        if not meal:
            raise HTTPException(status_code=404, detail="Target meal not found or not accessible")
    
    if entry_data.food_id != entry.food_id:
        food = db.query(Food).filter(Food.id == entry_data.food_id).first()
        if not food:
            raise HTTPException(status_code=404, detail="Food not found")
    
    food = db.query(Food).filter(Food.id == entry_data.food_id).first()
    
    nutrition = calculate_nutrition(food, entry_data.quantity_grams)
    
    entry.meal_id = entry_data.meal_id
    entry.food_id = entry_data.food_id
    entry.quantity_grams = entry_data.quantity_grams
    entry.total_calories = nutrition["total_calories"]
    entry.total_protein = nutrition["total_protein"]
    entry.total_carbs = nutrition["total_carbs"]
    entry.total_fat = nutrition["total_fat"]
    
    db.commit()
    db.refresh(entry)
    return entry

@router.delete("/{entry_id}")
def delete_food_entry(
    entry_id: int,
    current_user: UserJWT = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a food entry.
    
    WHY simple delete: No cascading needed, entries are leaf nodes
    """
    entry = db.query(FoodEntry)\
        .join(Meal)\
        .filter(
            FoodEntry.id == entry_id,
            Meal.user_id == current_user.sub
        ).first()
    
    if not entry:
        raise HTTPException(status_code=404, detail="Food entry not found")
    
    food_name = entry.food.name
    quantity = entry.quantity_grams
    
    db.delete(entry)
    db.commit()
    
    return {"message": f"Deleted {quantity}g of {food_name} from meal"}