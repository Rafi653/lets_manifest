/**
 * Blog Entry API service
 */

import { apiClient } from '../api/client';
import type { APIResponse } from '../types/api';
import type {
  BlogEntry,
  BlogEntryCreate,
  BlogEntryUpdate,
  PaginatedBlogEntries,
} from '../types/blogEntry';

export const blogEntryService = {
  /**
   * Create a new blog entry
   */
  async createBlogEntry(data: BlogEntryCreate): Promise<BlogEntry> {
    const response = await apiClient.post<APIResponse<BlogEntry>>(
      '/blog-entries',
      data
    );
    return response.data.data;
  },

  /**
   * Get all blog entries with optional filters and pagination
   */
  async getBlogEntries(params?: {
    status_filter?: string;
    page?: number;
    limit?: number;
  }): Promise<PaginatedBlogEntries> {
    const response = await apiClient.get<APIResponse<PaginatedBlogEntries>>(
      '/blog-entries',
      { params }
    );
    return response.data.data;
  },

  /**
   * Get a specific blog entry by ID
   */
  async getBlogEntry(entryId: string): Promise<BlogEntry> {
    const response = await apiClient.get<APIResponse<BlogEntry>>(
      `/blog-entries/${entryId}`
    );
    return response.data.data;
  },

  /**
   * Update a blog entry
   */
  async updateBlogEntry(entryId: string, data: BlogEntryUpdate): Promise<BlogEntry> {
    const response = await apiClient.put<APIResponse<BlogEntry>>(
      `/blog-entries/${entryId}`,
      data
    );
    return response.data.data;
  },

  /**
   * Delete a blog entry
   */
  async deleteBlogEntry(entryId: string): Promise<boolean> {
    const response = await apiClient.delete<APIResponse<{ deleted: boolean }>>(
      `/blog-entries/${entryId}`
    );
    return response.data.data.deleted;
  },

  /**
   * Generate a blog entry from a daily review
   */
  async generateFromReview(reviewId: string): Promise<BlogEntry> {
    const response = await apiClient.post<APIResponse<BlogEntry>>(
      `/blog-entries/generate-from-review/${reviewId}`
    );
    return response.data.data;
  },
};
