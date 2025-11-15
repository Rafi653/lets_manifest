/**
 * Type definitions for habit tracking and analytics.
 */

/**
 * Habit frequency types
 */
export type HabitFrequency = 'daily' | 'weekly' | 'custom';

/**
 * Base habit interface
 */
export interface Habit {
  id: string;
  user_id: string;
  name: string;
  description?: string;
  frequency: HabitFrequency;
  target_days?: number;
  category?: string;
  color?: string;
  icon?: string;
  reminder_time?: string;
  is_active: boolean;
  current_streak: number;
  longest_streak: number;
  total_completions: number;
  created_at: string;
  updated_at?: string;
}

/**
 * Habit entry for daily tracking
 */
export interface HabitEntry {
  id: string;
  habit_id: string;
  entry_date: string;
  completed: boolean;
  completed_at?: string;
  notes?: string;
  mood?: string;
  created_at: string;
  updated_at?: string;
}

/**
 * Streak information
 */
export interface StreakInfo {
  current_streak: number;
  longest_streak: number;
  last_completed_date?: string;
  is_active: boolean;
  streak_start_date?: string;
}

/**
 * Completion statistics
 */
export interface CompletionStats {
  total_completions: number;
  total_days_tracked: number;
  completion_rate: number;
  current_month_completions: number;
  current_week_completions: number;
}

/**
 * Comprehensive habit analytics
 */
export interface HabitAnalytics {
  habit_id: string;
  habit_name: string;
  frequency: HabitFrequency;
  streak_info: StreakInfo;
  completion_stats: CompletionStats;
  confidence_level: number;
  motivational_message: string;
}

/**
 * Daily completion data for visualization
 */
export interface DailyCompletionData {
  date: string;
  completed: boolean;
  mood?: string;
  notes?: string;
}

/**
 * Weekly progress summary
 */
export interface WeeklyProgress {
  week_start: string;
  week_end: string;
  completions: number;
  target: number;
  completion_rate: number;
}

/**
 * Monthly progress summary
 */
export interface MonthlyProgress {
  month: number;
  year: number;
  completions: number;
  target: number;
  completion_rate: number;
}

/**
 * Trend direction
 */
export type TrendDirection = 'improving' | 'stable' | 'declining' | 'no_data';

/**
 * Progress trends over time
 */
export interface ProgressTrends {
  daily_data: DailyCompletionData[];
  weekly_summaries: WeeklyProgress[];
  monthly_summaries: MonthlyProgress[];
  overall_trend: TrendDirection;
}

/**
 * Streak recovery information
 */
export interface StreakRecoveryInfo {
  can_recover: boolean;
  days_since_last_completion: number;
  recovery_deadline?: string;
  grace_period_days: number;
}

/**
 * Aggregated habit insights
 */
export interface HabitInsights {
  best_performing_habits: string[];
  needs_attention: string[];
  total_active_streaks: number;
  average_streak_length: number;
  overall_completion_rate: number;
  motivational_insights: string[];
}

/**
 * Request types
 */
export interface CreateHabitRequest {
  name: string;
  description?: string;
  frequency: HabitFrequency;
  target_days?: number;
  category?: string;
  color?: string;
  icon?: string;
  reminder_time?: string;
}

export interface UpdateHabitRequest {
  name?: string;
  description?: string;
  frequency?: HabitFrequency;
  target_days?: number;
  category?: string;
  color?: string;
  icon?: string;
  reminder_time?: string;
  is_active?: boolean;
}

export interface CreateHabitEntryRequest {
  entry_date: string;
  completed: boolean;
  notes?: string;
  mood?: string;
}
