/**
 * Food service for API calls
 */

import { apiClient } from '../api/client';
import {
  Food,
  CreateFoodRequest,
  UpdateFoodRequest,
} from '../types/food';
import { APIResponse, PaginatedResponse } from '../types/api';

/**
 * Food CRUD operations
 */
export const foodService = {
  /**
   * Create a new food entry
   */
  createFood: async (data: CreateFoodRequest): Promise<Food> => {
    const response = await apiClient.post<APIResponse<Food>>('/foods', data);
    return response.data.data;
  },

  /**
   * Get all food entries for the current user
   */
  getFoods: async (
    mealType?: string,
    startDate?: string,
    endDate?: string,
    page = 1,
    limit = 20
  ): Promise<PaginatedResponse<Food>> => {
    const params = new URLSearchParams();
    if (mealType) params.append('meal_type', mealType);
    if (startDate) params.append('start_date', startDate);
    if (endDate) params.append('end_date', endDate);
    params.append('page', String(page));
    params.append('limit', String(limit));

    const response = await apiClient.get<APIResponse<PaginatedResponse<Food>>>(
      `/foods?${params.toString()}`
    );
    return response.data.data;
  },

  /**
   * Get a specific food entry by ID
   */
  getFood: async (foodId: string): Promise<Food> => {
    const response = await apiClient.get<APIResponse<Food>>(
      `/foods/${foodId}`
    );
    return response.data.data;
  },

  /**
   * Update a food entry
   */
  updateFood: async (
    foodId: string,
    data: UpdateFoodRequest
  ): Promise<Food> => {
    const response = await apiClient.put<APIResponse<Food>>(
      `/foods/${foodId}`,
      data
    );
    return response.data.data;
  },

  /**
   * Delete a food entry
   */
  deleteFood: async (foodId: string): Promise<boolean> => {
    const response = await apiClient.delete<APIResponse<{ deleted: boolean }>>(
      `/foods/${foodId}`
    );
    return response.data.data.deleted;
  },
};

export default foodService;
