/**
 * Goal-related TypeScript types matching the backend API schemas
 */

export type GoalType = 'daily' | 'weekly' | 'monthly' | 'yearly' | 'life_goal';
export type GoalStatus = 'active' | 'completed' | 'cancelled' | 'paused' | 'in_progress';
export type MilestoneStatus = 'pending' | 'in_progress' | 'completed' | 'skipped';

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
  start_date: string | null; // ISO date string (nullable for life goals)
  end_date: string | null; // ISO date string (nullable for life goals)
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
  start_date?: string | null; // ISO date string (nullable for life goals)
  end_date?: string | null; // ISO date string (nullable for life goals)
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

// Life goal milestone types
export interface GoalMilestone {
  id: string;
  goal_id: string;
  title: string;
  description: string | null;
  order_index: number;
  status: MilestoneStatus;
  target_date: string | null; // ISO date string
  created_at: string; // ISO datetime string
  completed_at: string | null;
}

export interface GoalMilestoneCreate {
  title: string;
  description?: string | null;
  order_index?: number;
  target_date?: string | null; // ISO date string
}

export interface GoalMilestoneUpdate {
  title?: string;
  description?: string | null;
  order_index?: number;
  status?: MilestoneStatus;
  target_date?: string | null; // ISO date string
}

// Life goal analytics types
export interface LifeGoalSummary {
  total_goals: number;
  active_goals: number;
  completed_goals: number;
  cancelled_goals: number;
  completion_rate: number;
  goals_by_category: Record<string, number>;
  avg_days_to_complete: number | null;
}

export interface MilestoneStatistics {
  total_milestones: number;
  completed_milestones: number;
  in_progress_milestones: number;
  pending_milestones: number;
  skipped_milestones: number;
  completion_rate: number;
}

export interface GoalsByLifeArea {
  life_area: string;
  goal_count: number;
  goals: Array<{
    id: string;
    title: string;
    status: GoalStatus;
    priority: number;
    created_at: string | null;
    completed_at: string | null;
  }>;
}

// Life area categories
export const LIFE_AREAS = [
  'investment',
  'travel',
  'health',
  'career',
  'education',
  'relationships',
  'personal_growth',
  'paperwork',
  'home',
  'financial',
  'creative',
  'social',
  'spiritual',
  'other'
] as const;

export type LifeArea = typeof LIFE_AREAS[number];
