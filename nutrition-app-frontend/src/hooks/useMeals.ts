import { useState, useEffect } from 'react';
import { mealService } from '../services/api';
import type { Meal, MealType } from '../types/api';

export function useMeals(date?: string, mealType?: MealType) {
  const [meals, setMeals] = useState<Meal[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchMeals = async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await mealService.getAll({
        meal_date: date,
        meal_type: mealType,
        limit: 50
      });
      setMeals(result);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch meals');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMeals();
  }, [date, mealType]);

  const addMeal = (meal: Meal) => {
    setMeals(prev => [...prev, meal]);
  };

  const updateMeal = (updatedMeal: Meal) => {
    setMeals(prev => 
      prev.map(meal => meal.id === updatedMeal.id ? updatedMeal : meal)
    );
  };

  const removeMeal = (mealId: number) => {
    setMeals(prev => prev.filter(meal => meal.id !== mealId));
  };

  return {
    meals,
    loading,
    error,
    refetch: fetchMeals,
    addMeal,
    updateMeal,
    removeMeal
  };
}