/**
 * Notification-related TypeScript types matching the backend API schemas
 */

export type NotificationType = 'reminder' | 'goal_deadline' | 'goal_completed' | 'system';
export type NotificationStatus = 'pending' | 'sent' | 'failed' | 'cancelled';

export interface Notification {
  id: string;
  user_id: string;
  goal_id: string | null;
  title: string;
  message: string | null;
  notification_type: NotificationType;
  scheduled_time: string; // ISO datetime string
  sent_at: string | null; // ISO datetime string
  status: NotificationStatus;
  is_read: boolean;
  created_at: string; // ISO datetime string
}

export interface NotificationCreate {
  title: string;
  message?: string | null;
  notification_type: NotificationType;
  scheduled_time: string; // ISO datetime string
  goal_id?: string | null;
}

export interface NotificationUpdate {
  is_read?: boolean;
  status?: NotificationStatus;
}

export interface NotificationSettings {
  id: string;
  user_id: string;
  email_enabled: boolean;
  email_reminders: boolean;
  email_goal_updates: boolean;
  browser_enabled: boolean;
  browser_reminders: boolean;
  default_reminder_time: string; // HH:MM format
  reminder_before_hours: string;
  created_at: string; // ISO datetime string
  updated_at: string | null; // ISO datetime string
}

export interface NotificationSettingsCreate {
  email_enabled?: boolean;
  email_reminders?: boolean;
  email_goal_updates?: boolean;
  browser_enabled?: boolean;
  browser_reminders?: boolean;
  default_reminder_time?: string; // HH:MM format
  reminder_before_hours?: string;
}

export interface NotificationSettingsUpdate {
  email_enabled?: boolean;
  email_reminders?: boolean;
  email_goal_updates?: boolean;
  browser_enabled?: boolean;
  browser_reminders?: boolean;
  default_reminder_time?: string; // HH:MM format
  reminder_before_hours?: string;
}

export interface PaginatedNotifications {
  items: Notification[];
  total: number;
  page: number;
  limit: number;
  total_pages: number;
}
