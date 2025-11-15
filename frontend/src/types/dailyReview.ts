/**
 * Daily Review TypeScript types matching the backend API schemas
 */

export interface DailyReview {
  id: string;
  user_id: string;
  review_date: string; // ISO date string
  mood_rating: number | null; // 1-10
  energy_level: number | null; // 1-10
  productivity_rating: number | null; // 1-10
  sleep_hours: number | null; // 0-24
  sleep_quality: number | null; // 1-10
  water_intake_ml: number | null;
  screen_time_minutes: number | null;
  steps: number | null;
  accomplishments: string | null;
  challenges: string | null;
  lessons_learned: string | null;
  gratitude: string | null;
  tomorrow_intentions: string | null;
  highlights: string | null;
  created_at: string; // ISO datetime string
  updated_at: string | null;
}

export interface DailyReviewCreate {
  review_date: string; // ISO date string
  mood_rating?: number | null;
  energy_level?: number | null;
  productivity_rating?: number | null;
  sleep_hours?: number | null;
  sleep_quality?: number | null;
  water_intake_ml?: number | null;
  screen_time_minutes?: number | null;
  steps?: number | null;
  accomplishments?: string | null;
  challenges?: string | null;
  lessons_learned?: string | null;
  gratitude?: string | null;
  tomorrow_intentions?: string | null;
  highlights?: string | null;
}

export interface DailyReviewUpdate {
  mood_rating?: number | null;
  energy_level?: number | null;
  productivity_rating?: number | null;
  sleep_hours?: number | null;
  sleep_quality?: number | null;
  water_intake_ml?: number | null;
  screen_time_minutes?: number | null;
  steps?: number | null;
  accomplishments?: string | null;
  challenges?: string | null;
  lessons_learned?: string | null;
  gratitude?: string | null;
  tomorrow_intentions?: string | null;
  highlights?: string | null;
}

export interface PaginatedDailyReviews {
  items: DailyReview[];
  total: number;
  page: number;
  limit: number;
  total_pages: number;
}
