from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import date
from enum import Enum

# Enum for meal types - restricts valid values
class MealType(str, Enum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch" 
    DINNER = "dinner"
    SNACK = "snack"

# Base schema for Food - shared fields
class FoodBase(BaseModel):
    name: str
    calories_per_100g: float
    protein_per_100g: float
    carbs_per_100g: float
    fat_per_100g: float
    fiber_per_100g: Optional[float] = 0.0
    
    @validator('calories_per_100g', 'protein_per_100g', 'carbs_per_100g', 'fat_per_100g')
    def validate_positive(cls, value):
        if value < 0:
            raise ValueError('Nutritional values must be positive')
        return value

class FoodCreate(FoodBase):
    pass  

class FoodRead(FoodBase):
    id: int
    
    class Config:
        orm_mode = True  

class FoodEntryBase(BaseModel):
    food_id: int
    quantity_grams: float
    
    @validator('quantity_grams')
    def validate_quantity(cls, value):
        if value <= 0:
            raise ValueError('Quantity must be positive')
        return value

class FoodEntryCreate(FoodEntryBase):
    pass

class FoodEntryRead(FoodEntryBase):
    id: int
    meal_id: int
    total_calories: float
    total_protein: float
    total_carbs: float
    total_fat: float
    
    food: FoodRead
    
    class Config:
        orm_mode = True

class MealBase(BaseModel):
    date: date
    meal_type: MealType  # Uses enum for validation

class MealCreate(MealBase):
    pass

class MealRead(MealBase):
    id: int
    user_id: int
    
    food_entries: List[FoodEntryRead] = []
    
    class Config:
        orm_mode = True

class MealSummary(MealBase):
    id: int
    total_calories: float
    total_protein: float
    total_carbs: float
    total_fat: float
    entry_count: int  # How many foods in this meal