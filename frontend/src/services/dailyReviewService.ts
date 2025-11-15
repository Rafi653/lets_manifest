/**
 * Daily Review API service
 */

import { apiClient } from '../api/client';
import type { APIResponse } from '../types/api';
import type {
  DailyReview,
  DailyReviewCreate,
  DailyReviewUpdate,
  PaginatedDailyReviews,
} from '../types/dailyReview';

export const dailyReviewService = {
  /**
   * Create a new daily review
   */
  async createReview(data: DailyReviewCreate): Promise<DailyReview> {
    const response = await apiClient.post<APIResponse<DailyReview>>(
      '/daily-reviews',
      data
    );
    return response.data.data;
  },

  /**
   * Get all daily reviews with optional filters and pagination
   */
  async getReviews(params?: {
    start_date?: string;
    end_date?: string;
    page?: number;
    limit?: number;
  }): Promise<PaginatedDailyReviews> {
    const response = await apiClient.get<APIResponse<PaginatedDailyReviews>>(
      '/daily-reviews',
      { params }
    );
    return response.data.data;
  },

  /**
   * Get a specific daily review by ID
   */
  async getReview(reviewId: string): Promise<DailyReview> {
    const response = await apiClient.get<APIResponse<DailyReview>>(
      `/daily-reviews/${reviewId}`
    );
    return response.data.data;
  },

  /**
   * Update a daily review
   */
  async updateReview(reviewId: string, data: DailyReviewUpdate): Promise<DailyReview> {
    const response = await apiClient.put<APIResponse<DailyReview>>(
      `/daily-reviews/${reviewId}`,
      data
    );
    return response.data.data;
  },

  /**
   * Delete a daily review
   */
  async deleteReview(reviewId: string): Promise<boolean> {
    const response = await apiClient.delete<APIResponse<{ deleted: boolean }>>(
      `/daily-reviews/${reviewId}`
    );
    return response.data.data.deleted;
  },
};
