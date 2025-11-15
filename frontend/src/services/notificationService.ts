/**
 * Notification API service
 */

import { apiClient } from '../api/client';
import type { APIResponse } from '../types/api';
import type {
  Notification,
  NotificationCreate,
  NotificationUpdate,
  NotificationSettings,
  NotificationSettingsCreate,
  NotificationSettingsUpdate,
  PaginatedNotifications,
} from '../types/notification';

export const notificationService = {
  /**
   * Create a new notification
   */
  async createNotification(data: NotificationCreate): Promise<Notification> {
    const response = await apiClient.post<APIResponse<Notification>>(
      '/notifications',
      data
    );
    return response.data.data;
  },

  /**
   * Get all notifications with optional filters and pagination
   */
  async getNotifications(params?: {
    is_read?: boolean;
    page?: number;
    limit?: number;
  }): Promise<PaginatedNotifications> {
    const response = await apiClient.get<APIResponse<PaginatedNotifications>>(
      '/notifications',
      { params }
    );
    return response.data.data;
  },

  /**
   * Get a specific notification by ID
   */
  async getNotification(notificationId: string): Promise<Notification> {
    const response = await apiClient.get<APIResponse<Notification>>(
      `/notifications/${notificationId}`
    );
    return response.data.data;
  },

  /**
   * Update a notification
   */
  async updateNotification(
    notificationId: string,
    data: NotificationUpdate
  ): Promise<Notification> {
    const response = await apiClient.put<APIResponse<Notification>>(
      `/notifications/${notificationId}`,
      data
    );
    return response.data.data;
  },

  /**
   * Mark a notification as read
   */
  async markAsRead(notificationId: string): Promise<Notification> {
    const response = await apiClient.post<APIResponse<Notification>>(
      `/notifications/${notificationId}/read`
    );
    return response.data.data;
  },

  /**
   * Delete a notification
   */
  async deleteNotification(notificationId: string): Promise<boolean> {
    const response = await apiClient.delete<APIResponse<{ deleted: boolean }>>(
      `/notifications/${notificationId}`
    );
    return response.data.data.deleted;
  },

  /**
   * Get notification settings for current user
   */
  async getSettings(): Promise<NotificationSettings> {
    const response = await apiClient.get<APIResponse<NotificationSettings>>(
      '/notifications/settings/me'
    );
    return response.data.data;
  },

  /**
   * Create notification settings
   */
  async createSettings(
    data: NotificationSettingsCreate
  ): Promise<NotificationSettings> {
    const response = await apiClient.post<APIResponse<NotificationSettings>>(
      '/notifications/settings',
      data
    );
    return response.data.data;
  },

  /**
   * Update notification settings
   */
  async updateSettings(
    data: NotificationSettingsUpdate
  ): Promise<NotificationSettings> {
    const response = await apiClient.put<APIResponse<NotificationSettings>>(
      '/notifications/settings/me',
      data
    );
    return response.data.data;
  },

  /**
   * Request browser notification permission
   */
  async requestPermission(): Promise<NotificationPermission> {
    if (!('Notification' in window)) {
      throw new Error('Browser notifications are not supported');
    }

    if (Notification.permission === 'granted') {
      return 'granted';
    }

    if (Notification.permission !== 'denied') {
      const permission = await Notification.requestPermission();
      return permission;
    }

    return Notification.permission;
  },

  /**
   * Show browser notification
   */
  showBrowserNotification(title: string, options?: NotificationOptions): void {
    if (Notification.permission === 'granted') {
      new Notification(title, options);
    }
  },
};
