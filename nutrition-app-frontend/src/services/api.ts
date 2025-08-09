import api from '../api';
import type { 
  Food, FoodCreate, 
  Meal, MealCreate, 
  FoodEntry, FoodEntryCreate,
  MealType 
} from '../types/api';

// Food API Service
export const foodService = {
  // GET /api/foods/ - Get all foods with search and pagination
  getAll: async (params?: { 
    search?: string; 
    skip?: number; 
    limit?: number; 
  }) => {
    const response = await api.get('/api/foods/', { params });
    return response.data as Food[];
  },

  // GET /api/foods/{id} - Get single food by ID
  getById: async (id: number) => {
    const response = await api.get(`/api/foods/${id}`);
    return response.data as Food;
  },

  // POST /api/foods/ - Create new food
  create: async (foodData: FoodCreate) => {
    const response = await api.post('/api/foods/', foodData);
    return response.data as Food;
  },

  // PUT /api/foods/{id} - Update existing food
  update: async (id: number, foodData: FoodCreate) => {
    const response = await api.put(`/api/foods/${id}`, foodData);
    return response.data as Food;
  },

  // DELETE /api/foods/{id} - Delete food
  delete: async (id: number) => {
    const response = await api.delete(`/api/foods/${id}`);
    return response.data;
  }
};

// Meal API Service
export const mealService = {
  // GET /api/meals/ - Get user's meals with filtering
  getAll: async (params?: {
    meal_date?: string;
    meal_type?: MealType;
    skip?: number;
    limit?: number;
  }) => {
    const response = await api.get('/api/meals/', { params });
    return response.data as Meal[];
  },

  // GET /api/meals/{id} - Get single meal with food entries
  getById: async (id: number) => {
    const response = await api.get(`/api/meals/${id}`);
    return response.data as Meal;
  },

  // POST /api/meals/ - Create new meal
  create: async (mealData: MealCreate) => {
    const response = await api.post('/api/meals/', mealData);
    return response.data as Meal;
  },

  // PUT /api/meals/{id} - Update meal
  update: async (id: number, mealData: MealCreate) => {
    const response = await api.put(`/api/meals/${id}`, mealData);
    return response.data as Meal;
  },

  // DELETE /api/meals/{id} - Delete meal and all its food entries
  delete: async (id: number) => {
    const response = await api.delete(`/api/meals/${id}`);
    return response.data;
  }
};

// Food Entry API Service  
export const foodEntryService = {
  // GET /api/food-entries/ - Get food entries with filtering
  getAll: async (params?: {
    meal_id?: number;
    food_id?: number;
    skip?: number;
    limit?: number;
  }) => {
    const response = await api.get('/api/food-entries/', { params });
    return response.data as FoodEntry[];
  },

  // GET /api/food-entries/{id} - Get single food entry
  getById: async (id: number) => {
    const response = await api.get(`/api/food-entries/${id}`);
    return response.data as FoodEntry;
  },

  // POST /api/food-entries/ - Add food to meal
  create: async (entryData: FoodEntryCreate) => {
    const response = await api.post('/api/food-entries/', entryData);
    return response.data as FoodEntry;
  },

  // PUT /api/food-entries/{id} - Update food entry quantity
  update: async (id: number, entryData: FoodEntryCreate) => {
    const response = await api.put(`/api/food-entries/${id}`, entryData);
    return response.data as FoodEntry;
  },

  // DELETE /api/food-entries/{id} - Remove food from meal
  delete: async (id: number) => {
    const response = await api.delete(`/api/food-entries/${id}`);
    return response.data;
  }
};