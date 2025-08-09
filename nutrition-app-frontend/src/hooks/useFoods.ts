import { useState, useEffect } from 'react';
import { foodService } from '../services/api';
import type { Food } from '../types/api';

export function useFoods(initialSearch: string = '') {
  const [foods, setFoods] = useState<Food[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState(initialSearch);

  const fetchFoods = async (searchTerm: string = search) => {
    setLoading(true);
    setError(null);
    try {
      const result = await foodService.getAll({ 
        search: searchTerm || undefined,
        limit: 50 
      });
      setFoods(result);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch foods');
    } finally {
      setLoading(false);
    }
  };

  // Debounced search - wait 300ms after user stops typing
  useEffect(() => {
    const timeoutId = setTimeout(() => {
      fetchFoods(search);
    }, 300);

    return () => clearTimeout(timeoutId);
  }, [search]);

  // Initial fetch
  useEffect(() => {
    fetchFoods();
  }, []);

  return {
    foods,
    loading,
    error,
    search,
    setSearch,
    refetch: () => fetchFoods(search)
  };
}