/**
 * Custom hook for managing notifications
 */

import { useState, useEffect, useCallback } from 'react';
import { notificationService } from '../services/notificationService';
import type { Notification } from '../types/notification';

export interface UseNotificationsOptions {
  autoFetch?: boolean;
  isRead?: boolean;
  page?: number;
  limit?: number;
}

export const useNotifications = (options: UseNotificationsOptions = {}) => {
  const { autoFetch = true, isRead, page = 1, limit = 20 } = options;

  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [total, setTotal] = useState(0);
  const [totalPages, setTotalPages] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const [unreadCount, setUnreadCount] = useState(0);

  const fetchNotifications = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const data = await notificationService.getNotifications({
        is_read: isRead,
        page,
        limit,
      });

      setNotifications(data.items);
      setTotal(data.total);
      setTotalPages(data.total_pages);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to fetch notifications'));
    } finally {
      setLoading(false);
    }
  }, [isRead, page, limit]);

  const fetchUnreadCount = useCallback(async () => {
    try {
      const data = await notificationService.getNotifications({
        is_read: false,
        page: 1,
        limit: 1,
      });
      setUnreadCount(data.total);
    } catch (err) {
      console.error('Failed to fetch unread count:', err);
    }
  }, []);

  const markAsRead = useCallback(
    async (notificationId: string) => {
      try {
        await notificationService.markAsRead(notificationId);
        
        // Update local state
        setNotifications((prev) =>
          prev.map((n) =>
            n.id === notificationId ? { ...n, is_read: true } : n
          )
        );
        
        // Update unread count
        setUnreadCount((prev) => Math.max(0, prev - 1));
      } catch (err) {
        setError(err instanceof Error ? err : new Error('Failed to mark as read'));
      }
    },
    []
  );

  const deleteNotification = useCallback(
    async (notificationId: string) => {
      try {
        await notificationService.deleteNotification(notificationId);
        
        // Update local state
        setNotifications((prev) => prev.filter((n) => n.id !== notificationId));
        setTotal((prev) => prev - 1);
      } catch (err) {
        setError(err instanceof Error ? err : new Error('Failed to delete notification'));
      }
    },
    []
  );

  const requestPermission = useCallback(async () => {
    try {
      const permission = await notificationService.requestPermission();
      return permission === 'granted';
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to request permission'));
      return false;
    }
  }, []);

  useEffect(() => {
    if (autoFetch) {
      fetchNotifications();
      fetchUnreadCount();
    }
  }, [autoFetch, fetchNotifications, fetchUnreadCount]);

  return {
    notifications,
    total,
    totalPages,
    loading,
    error,
    unreadCount,
    fetchNotifications,
    fetchUnreadCount,
    markAsRead,
    deleteNotification,
    requestPermission,
  };
};
