/**
 * Goal-related TypeScript types matching the backend API schemas
 */

export type GoalType = 'daily' | 'weekly' | 'monthly' | 'yearly';
export type GoalStatus = 'active' | 'completed' | 'cancelled' | 'paused';

export interface Goal {
  id: string;
  user_id: string;
  title: string;
  description: string | null;
  goal_type: GoalType;
  category: string | null;
  target_value: number | null;
  target_unit: string | null;
  current_value: number;
  start_date: string; // ISO date string
  end_date: string; // ISO date string
  priority: number; // 0-5
  status: GoalStatus;
  is_recurring: boolean;
  recurrence_pattern: string | null;
  parent_goal_id: string | null;
  reminder_enabled: boolean;
  reminder_time: string | null; // HH:MM format
  reminder_days_before: number | null;
  created_at: string; // ISO datetime string
  updated_at: string | null;
  completed_at: string | null;
}

export interface GoalCreate {
  title: string;
  description?: string | null;
  goal_type: GoalType;
  category?: string | null;
  target_value?: number | null;
  target_unit?: string | null;
  start_date: string; // ISO date string
  end_date: string; // ISO date string
  priority?: number; // 0-5
  is_recurring?: boolean;
  recurrence_pattern?: string | null;
  parent_goal_id?: string | null;
  reminder_enabled?: boolean;
  reminder_time?: string | null; // HH:MM format
  reminder_days_before?: number | null;
}

export interface GoalUpdate {
  title?: string;
  description?: string | null;
  category?: string | null;
  target_value?: number | null;
  target_unit?: string | null;
  end_date?: string;
  status?: GoalStatus;
  priority?: number;
  current_value?: number;
  reminder_enabled?: boolean;
  reminder_time?: string | null; // HH:MM format
  reminder_days_before?: number | null;
}

export interface GoalProgress {
  id: string;
  goal_id: string;
  progress_date: string; // ISO date string
  value: number;
  notes: string | null;
  percentage: number | null;
  created_at: string; // ISO datetime string
}

export interface GoalProgressCreate {
  progress_date: string; // ISO date string
  value: number;
  notes?: string | null;
}

export interface PaginatedGoals {
  items: Goal[];
  total: number;
  page: number;
  limit: number;
  total_pages: number;
}
