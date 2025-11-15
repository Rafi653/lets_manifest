/**
 * Habit service for API calls
 */

import { apiClient } from '../api/client';
import {
  Habit,
  HabitEntry,
  HabitAnalytics,
  ProgressTrends,
  StreakRecoveryInfo,
  HabitInsights,
  CreateHabitRequest,
  UpdateHabitRequest,
  CreateHabitEntryRequest,
} from '../types/habit';
import { APIResponse, PaginatedResponse } from '../types/api';

/**
 * Habit CRUD operations
 */
export const habitService = {
  /**
   * Create a new habit
   */
  createHabit: async (data: CreateHabitRequest): Promise<Habit> => {
    const response = await apiClient.post<APIResponse<Habit>>('/habits', data);
    return response.data.data;
  },

  /**
   * Get all habits for the current user
   */
  getHabits: async (
    isActive?: boolean,
    page = 1,
    limit = 20
  ): Promise<PaginatedResponse<Habit>> => {
    const params = new URLSearchParams();
    if (isActive !== undefined) params.append('is_active', String(isActive));
    params.append('page', String(page));
    params.append('limit', String(limit));

    const response = await apiClient.get<APIResponse<PaginatedResponse<Habit>>>(
      `/habits?${params.toString()}`
    );
    return response.data.data;
  },

  /**
   * Get a specific habit by ID
   */
  getHabit: async (habitId: string): Promise<Habit> => {
    const response = await apiClient.get<APIResponse<Habit>>(
      `/habits/${habitId}`
    );
    return response.data.data;
  },

  /**
   * Update a habit
   */
  updateHabit: async (
    habitId: string,
    data: UpdateHabitRequest
  ): Promise<Habit> => {
    const response = await apiClient.put<APIResponse<Habit>>(
      `/habits/${habitId}`,
      data
    );
    return response.data.data;
  },

  /**
   * Delete a habit
   */
  deleteHabit: async (habitId: string): Promise<boolean> => {
    const response = await apiClient.delete<APIResponse<{ deleted: boolean }>>(
      `/habits/${habitId}`
    );
    return response.data.data.deleted;
  },

  /**
   * Create a habit entry
   */
  createEntry: async (
    habitId: string,
    data: CreateHabitEntryRequest
  ): Promise<HabitEntry> => {
    const response = await apiClient.post<APIResponse<HabitEntry>>(
      `/habits/${habitId}/entries`,
      data
    );
    return response.data.data;
  },

  /**
   * Get entries for a habit
   */
  getEntries: async (
    habitId: string,
    page = 1,
    limit = 20
  ): Promise<HabitEntry[]> => {
    const response = await apiClient.get<APIResponse<HabitEntry[]>>(
      `/habits/${habitId}/entries?page=${page}&limit=${limit}`
    );
    return response.data.data;
  },

  /**
   * Reset a habit's streak
   */
  resetStreak: async (habitId: string): Promise<Habit> => {
    const response = await apiClient.post<APIResponse<Habit>>(
      `/habits/${habitId}/reset-streak`
    );
    return response.data.data;
  },

  /**
   * Recover a broken streak
   */
  recoverStreak: async (
    habitId: string,
    recoveryDate: string
  ): Promise<HabitEntry> => {
    const response = await apiClient.post<APIResponse<HabitEntry>>(
      `/habits/${habitId}/recover-streak?recovery_date=${recoveryDate}`
    );
    return response.data.data;
  },
};

/**
 * Habit analytics operations
 */
export const habitAnalyticsService = {
  /**
   * Get comprehensive analytics for a habit
   */
  getAnalytics: async (habitId: string): Promise<HabitAnalytics> => {
    const response = await apiClient.get<APIResponse<HabitAnalytics>>(
      `/habits/${habitId}/analytics`
    );
    return response.data.data;
  },

  /**
   * Get progress trends over time
   */
  getProgressTrends: async (
    habitId: string,
    days = 90
  ): Promise<ProgressTrends> => {
    const response = await apiClient.get<APIResponse<ProgressTrends>>(
      `/habits/${habitId}/progress?days=${days}`
    );
    return response.data.data;
  },

  /**
   * Check streak recovery eligibility
   */
  checkStreakRecovery: async (
    habitId: string,
    graceDays = 1
  ): Promise<StreakRecoveryInfo> => {
    const response = await apiClient.get<APIResponse<StreakRecoveryInfo>>(
      `/habits/${habitId}/streak-recovery?grace_days=${graceDays}`
    );
    return response.data.data;
  },

  /**
   * Get aggregated insights for all habits
   */
  getUserInsights: async (): Promise<HabitInsights> => {
    const response = await apiClient.get<APIResponse<HabitInsights>>(
      '/habits/insights'
    );
    return response.data.data;
  },
};

export default habitService;
