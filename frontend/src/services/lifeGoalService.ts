/**
 * Life Goals API service
 * Handles life goal specific operations including milestones and analytics
 */

import { apiClient } from '../api/client';
import type { APIResponse } from '../types/api';
import type {
  Goal,
  GoalCreate,
  GoalUpdate,
  GoalMilestone,
  GoalMilestoneCreate,
  GoalMilestoneUpdate,
  PaginatedGoals,
  LifeGoalSummary,
  MilestoneStatistics,
  GoalsByLifeArea,
} from '../types/goal';

export const lifeGoalService = {
  /**
   * Create a new life goal
   */
  async createLifeGoal(data: GoalCreate): Promise<Goal> {
    const lifeGoalData = { ...data, goal_type: 'life_goal' as const };
    const response = await apiClient.post<APIResponse<Goal>>('/goals', lifeGoalData);
    return response.data.data;
  },

  /**
   * Get all life goals with optional filters and pagination
   */
  async getLifeGoals(params?: {
    status_filter?: string;
    page?: number;
    limit?: number;
  }): Promise<PaginatedGoals> {
    const response = await apiClient.get<APIResponse<PaginatedGoals>>('/goals', {
      params: {
        ...params,
        goal_type: 'life_goal',
      },
    });
    return response.data.data;
  },

  /**
   * Get a specific life goal by ID
   */
  async getLifeGoal(goalId: string): Promise<Goal> {
    const response = await apiClient.get<APIResponse<Goal>>(`/goals/${goalId}`);
    return response.data.data;
  },

  /**
   * Update a life goal
   */
  async updateLifeGoal(goalId: string, data: GoalUpdate): Promise<Goal> {
    const response = await apiClient.put<APIResponse<Goal>>(`/goals/${goalId}`, data);
    return response.data.data;
  },

  /**
   * Delete a life goal
   */
  async deleteLifeGoal(goalId: string): Promise<boolean> {
    const response = await apiClient.delete<APIResponse<{ deleted: boolean }>>(
      `/goals/${goalId}`
    );
    return response.data.data.deleted;
  },

  // Milestone operations

  /**
   * Create a milestone for a life goal
   */
  async createMilestone(
    goalId: string,
    data: GoalMilestoneCreate
  ): Promise<GoalMilestone> {
    const response = await apiClient.post<APIResponse<GoalMilestone>>(
      `/goals/${goalId}/milestones`,
      data
    );
    return response.data.data;
  },

  /**
   * Get milestones for a life goal
   */
  async getMilestones(
    goalId: string,
    params?: { page?: number; limit?: number }
  ): Promise<GoalMilestone[]> {
    const response = await apiClient.get<APIResponse<GoalMilestone[]>>(
      `/goals/${goalId}/milestones`,
      { params }
    );
    return response.data.data;
  },

  /**
   * Update a milestone
   */
  async updateMilestone(
    goalId: string,
    milestoneId: string,
    data: GoalMilestoneUpdate
  ): Promise<GoalMilestone> {
    const response = await apiClient.put<APIResponse<GoalMilestone>>(
      `/goals/${goalId}/milestones/${milestoneId}`,
      data
    );
    return response.data.data;
  },

  /**
   * Delete a milestone
   */
  async deleteMilestone(goalId: string, milestoneId: string): Promise<boolean> {
    const response = await apiClient.delete<APIResponse<{ deleted: boolean }>>(
      `/goals/${goalId}/milestones/${milestoneId}`
    );
    return response.data.data.deleted;
  },

  // Analytics operations

  /**
   * Get summary statistics for user's life goals
   */
  async getLifeGoalSummary(): Promise<LifeGoalSummary> {
    const response = await apiClient.get<APIResponse<LifeGoalSummary>>(
      '/analytics/life-goals/summary'
    );
    return response.data.data;
  },

  /**
   * Get milestone statistics
   * If goalId is provided, returns stats for that specific goal
   * Otherwise returns stats across all user's life goals
   */
  async getMilestoneStatistics(goalId?: string): Promise<MilestoneStatistics> {
    const response = await apiClient.get<APIResponse<MilestoneStatistics>>(
      '/analytics/life-goals/milestones/statistics',
      {
        params: goalId ? { goal_id: goalId } : undefined,
      }
    );
    return response.data.data;
  },

  /**
   * Get life goals grouped by life area/category
   */
  async getGoalsByLifeArea(): Promise<GoalsByLifeArea[]> {
    const response = await apiClient.get<APIResponse<GoalsByLifeArea[]>>(
      '/analytics/life-goals/by-life-area'
    );
    return response.data.data;
  },
};
