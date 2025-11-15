/**
 * Workout service for API calls
 */

import { apiClient } from '../api/client';
import type {
  Workout,
  CreateWorkoutRequest,
  UpdateWorkoutRequest,
} from '../types/workout';
import type { APIResponse, PaginatedResponse } from '../types/api';

/**
 * Workout CRUD operations
 */
export const workoutService = {
  /**
   * Create a new workout with exercises
   */
  createWorkout: async (data: CreateWorkoutRequest): Promise<Workout> => {
    const response = await apiClient.post<APIResponse<Workout>>('/workouts', data);
    return response.data.data;
  },

  /**
   * Get all workouts for the current user
   */
  getWorkouts: async (
    workoutType?: string,
    startDate?: string,
    endDate?: string,
    page = 1,
    limit = 20
  ): Promise<PaginatedResponse<Workout>> => {
    const params = new URLSearchParams();
    if (workoutType) params.append('workout_type', workoutType);
    if (startDate) params.append('start_date', startDate);
    if (endDate) params.append('end_date', endDate);
    params.append('page', String(page));
    params.append('limit', String(limit));

    const response = await apiClient.get<APIResponse<PaginatedResponse<Workout>>>(
      `/workouts?${params.toString()}`
    );
    return response.data.data;
  },

  /**
   * Get a specific workout by ID
   */
  getWorkout: async (workoutId: string): Promise<Workout> => {
    const response = await apiClient.get<APIResponse<Workout>>(
      `/workouts/${workoutId}`
    );
    return response.data.data;
  },

  /**
   * Update a workout
   */
  updateWorkout: async (
    workoutId: string,
    data: UpdateWorkoutRequest
  ): Promise<Workout> => {
    const response = await apiClient.put<APIResponse<Workout>>(
      `/workouts/${workoutId}`,
      data
    );
    return response.data.data;
  },

  /**
   * Delete a workout
   */
  deleteWorkout: async (workoutId: string): Promise<boolean> => {
    const response = await apiClient.delete<APIResponse<{ deleted: boolean }>>(
      `/workouts/${workoutId}`
    );
    return response.data.data.deleted;
  },
};

export default workoutService;
