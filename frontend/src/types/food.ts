/**
 * Type definitions for food tracking.
 */

/**
 * Meal type options
 */
export type MealType = 'breakfast' | 'lunch' | 'dinner' | 'snack';

/**
 * Food entry interface
 */
export interface Food {
  id: string;
  user_id: string;
  meal_date: string; // ISO date string
  meal_time?: string; // Time string
  meal_type: MealType;
  food_name: string;
  portion_size?: string;
  calories?: number;
  protein_grams?: number;
  carbs_grams?: number;
  fats_grams?: number;
  fiber_grams?: number;
  sugar_grams?: number;
  sodium_mg?: number;
  notes?: string;
  is_favorite: boolean;
  created_at: string;
  updated_at?: string;
}

/**
 * Request types
 */
export interface CreateFoodRequest {
  meal_date: string;
  meal_time?: string;
  meal_type: MealType;
  food_name: string;
  portion_size?: string;
  calories?: number;
  protein_grams?: number;
  carbs_grams?: number;
  fats_grams?: number;
  fiber_grams?: number;
  sugar_grams?: number;
  sodium_mg?: number;
  notes?: string;
  is_favorite?: boolean;
}

export interface UpdateFoodRequest {
  meal_time?: string;
  food_name?: string;
  portion_size?: string;
  calories?: number;
  protein_grams?: number;
  carbs_grams?: number;
  fats_grams?: number;
  fiber_grams?: number;
  sugar_grams?: number;
  sodium_mg?: number;
  notes?: string;
  is_favorite?: boolean;
}

/**
 * Food statistics
 */
export interface FoodStats {
  total_calories: number;
  total_protein: number;
  total_carbs: number;
  total_fats: number;
  meal_count: number;
}
