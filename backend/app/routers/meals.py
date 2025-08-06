from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.core.database import get_db
from app.models.nutrition import Meal
from app.schemas.nutrition import MealCreate, MealRead, MealType
from app.dependencies.supabase_auth import get_current_user
from app.schemas.user import UserJWT

router = APIRouter(prefix="/meals", tags=["Meals"])

@router.get("/", response_model=List[MealRead])
def get_meals(
    meal_date: Optional[date] = Query(None, description="Filter by specific date"),
    meal_type: Optional[MealType] = Query(None, description="Filter by meal type"),
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    current_user: UserJWT = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's meals with optional filtering by date and type.
    
    WHY we filter by user: Security - users should only see their own meals
    WHY optional filters: Flexibility - sometimes you want all meals, sometimes just breakfast
    WHY pagination: Performance - large datasets need chunking
    """
    query = db.query(Meal).filter(Meal.user_id == current_user.sub)
    
    if meal_date:
        query = query.filter(Meal.date == meal_date)
    
    if meal_type:
        query = query.filter(Meal.meal_type == meal_type.value)
    
    query = query.order_by(Meal.date.desc(), Meal.meal_type)
    
    meals = query.offset(skip).limit(limit).all()
    return meals

@router.get("/{meal_id}", response_model=MealRead)
def get_meal(
    meal_id: int,
    current_user: UserJWT = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific meal by ID.
    
    WHY check ownership: Security - prevent users accessing others' meals
    """
    meal = db.query(Meal).filter(
        Meal.id == meal_id,
        Meal.user_id == current_user.sub  
    ).first()
    
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    
    return meal

@router.post("/", response_model=MealRead, status_code=201)
def create_meal(
    meal_data: MealCreate,
    current_user: UserJWT = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new meal for the current user.
    
    WHY auto-assign user_id: Security - can't create meals for other users
    WHY check duplicates: Business logic - prevent multiple breakfasts on same day
    """
    existing = db.query(Meal).filter(
        Meal.user_id == current_user.sub,
        Meal.date == meal_data.date,
        Meal.meal_type == meal_data.meal_type.value
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=409, 
            detail=f"You already have a {meal_data.meal_type.value} meal on {meal_data.date}"
        )
    
    new_meal = Meal(
        user_id=current_user.sub,  
        date=meal_data.date,
        meal_type=meal_data.meal_type.value
    )
    
    db.add(new_meal)
    db.commit()
    db.refresh(new_meal)  
    
    return new_meal

@router.put("/{meal_id}", response_model=MealRead)
def update_meal(
    meal_id: int,
    meal_data: MealCreate,
    current_user: UserJWT = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update an existing meal.
    
    WHY check ownership first: Security before business logic
    WHY check conflicts on update: Prevent duplicate meals after editing
    """
    meal = db.query(Meal).filter(
        Meal.id == meal_id,
        Meal.user_id == current_user.sub
    ).first()
    
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")

    if meal_data.date != meal.date or meal_data.meal_type.value != meal.meal_type:
        existing = db.query(Meal).filter(
            Meal.user_id == current_user.sub,
            Meal.date == meal_data.date,
            Meal.meal_type == meal_data.meal_type.value,
            Meal.id != meal_id  
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=409,
                detail=f"You already have a {meal_data.meal_type.value} meal on {meal_data.date}"
            )
    
    meal.date = meal_data.date
    meal.meal_type = meal_data.meal_type.value
    
    db.commit()
    db.refresh(meal)
    return meal

@router.delete("/{meal_id}")
def delete_meal(
    meal_id: int,
    current_user: UserJWT = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a meal and all its food entries.
    
    WHY cascade delete: When meal is gone, its entries become meaningless
    This is handled by the database relationship: cascade="all, delete-orphan"
    """
    meal = db.query(Meal).filter(
        Meal.id == meal_id,
        Meal.user_id == current_user.sub
    ).first()
    
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    
    db.delete(meal)  
    db.commit()
    
    return {"message": f"{meal.meal_type.title()} meal on {meal.date} deleted successfully"}