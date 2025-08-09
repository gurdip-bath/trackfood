export interface Food {
  id: number;
  name: string;
  calories_per_100g: number;
  protein_per_100g: number;
  carbs_per_100g: number;
  fat_per_100g: number;
  fiber_per_100g: number;
}

export interface FoodCreate {
  name: string;
  calories_per_100g: number;
  protein_per_100g: number;
  carbs_per_100g: number;
  fat_per_100g: number;
  fiber_per_100g?: number;
}

export type MealType = 'breakfast' | 'lunch' | 'dinner' | 'snack';

export interface Meal {
  id: number;
  user_id: number;
  date: string; // ISO date string
  meal_type: MealType;
  food_entries: FoodEntry[];
}

export interface MealCreate {
  date: string;
  meal_type: MealType;
}

export interface FoodEntry {
  id: number;
  meal_id: number;
  food_id: number;
  quantity_grams: number;
  total_calories: number;
  total_protein: number;
  total_carbs: number;
  total_fat: number;
  food: Food;
}

export interface FoodEntryCreate {
  meal_id: number;
  food_id: number;
  quantity_grams: number;
}

export interface ApiError {
  detail: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
}