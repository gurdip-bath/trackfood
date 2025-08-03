from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Food(Base):
    __tablename__ = "foods"  
    
    id = Column(Integer, primary_key=True, index=True)
    
    # index=True creates a database index for faster queries
    name = Column(String, nullable=False, index=True)
    
    # Nutritional values per 100g (standardized portion)
    calories_per_100g = Column(Float, nullable=False)
    protein_per_100g = Column(Float, nullable=False)  
    carbs_per_100g = Column(Float, nullable=False)      
    fat_per_100g = Column(Float, nullable=False)      
    
    # Optional: fiber, sugar, sodium, etc. - add later if needed
    fiber_per_100g = Column(Float, default=0.0)
    
    food_entries = relationship("FoodEntry", back_populates="food")

class Meal(Base):
    __tablename__ = "meals"
    
    id = Column(Integer, primary_key=True, index=True)
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    date = Column(Date, nullable=False, index=True)  
    
    meal_type = Column(String, nullable=False)
    
    created_at = Column(DateTime, server_default=func.now())
    
    user = relationship("User", back_populates="meals")
    
    food_entries = relationship("FoodEntry", back_populates="meal", cascade="all, delete-orphan")

class FoodEntry(Base):
    __tablename__ = "food_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    
    meal_id = Column(Integer, ForeignKey("meals.id"), nullable=False)
    food_id = Column(Integer, ForeignKey("foods.id"), nullable=False)
    
    quantity_grams = Column(Float, nullable=False)
    
    # We store these to avoid recalculating every time
    total_calories = Column(Float, nullable=False)
    total_protein = Column(Float, nullable=False)
    total_carbs = Column(Float, nullable=False)
    total_fat = Column(Float, nullable=False)
    
    # Relationships
    meal = relationship("Meal", back_populates="food_entries")
    food = relationship("Food", back_populates="food_entries")