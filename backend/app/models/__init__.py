# Import all models so they're registered with SQLAlchemy
from .user import User
from .nutrition import Food, Meal, FoodEntry

# Export them so other files can import easily
__all__ = ["User", "Food", "Meal", "FoodEntry"]