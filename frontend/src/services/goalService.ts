/**
 * Goal API service
 */

import { apiClient } from '../api/client';
import type { APIResponse } from '../types/api';
import type {
  Goal,
  GoalCreate,
  GoalUpdate,
  GoalProgress,
  GoalProgressCreate,
  PaginatedGoals,
} from '../types/goal';

export const goalService = {
  /**
   * Create a new goal
   */
  async createGoal(data: GoalCreate): Promise<Goal> {
    const response = await apiClient.post<APIResponse<Goal>>('/goals', data);
    return response.data.data;
  },

  /**
   * Get all goals with optional filters and pagination
   */
  async getGoals(params?: {
    goal_type?: string;
    status_filter?: string;
    page?: number;
    limit?: number;
  }): Promise<PaginatedGoals> {
    const response = await apiClient.get<APIResponse<PaginatedGoals>>('/goals', {
      params,
    });
    return response.data.data;
  },

  /**
   * Get a specific goal by ID
   */
  async getGoal(goalId: string): Promise<Goal> {
    const response = await apiClient.get<APIResponse<Goal>>(`/goals/${goalId}`);
    return response.data.data;
  },

  /**
   * Update a goal
   */
  async updateGoal(goalId: string, data: GoalUpdate): Promise<Goal> {
    const response = await apiClient.put<APIResponse<Goal>>(`/goals/${goalId}`, data);
    return response.data.data;
  },

  /**
   * Delete a goal
   */
  async deleteGoal(goalId: string): Promise<boolean> {
    const response = await apiClient.delete<APIResponse<{ deleted: boolean }>>(
      `/goals/${goalId}`
    );
    return response.data.data.deleted;
  },

  /**
   * Add progress to a goal
   */
  async addProgress(goalId: string, data: GoalProgressCreate): Promise<GoalProgress> {
    const response = await apiClient.post<APIResponse<GoalProgress>>(
      `/goals/${goalId}/progress`,
      data
    );
    return response.data.data;
  },

  /**
   * Get progress entries for a goal
   */
  async getGoalProgress(
    goalId: string,
    params?: { page?: number; limit?: number }
  ): Promise<GoalProgress[]> {
    const response = await apiClient.get<APIResponse<GoalProgress[]>>(
      `/goals/${goalId}/progress`,
      { params }
    );
    return response.data.data;
  },
};
