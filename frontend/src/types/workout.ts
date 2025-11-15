/**
 * Type definitions for workout tracking.
 */

/**
 * Workout intensity levels
 */
export type WorkoutIntensity = 'low' | 'medium' | 'high';

/**
 * Weight unit options
 */
export type WeightUnit = 'lbs' | 'kg';

/**
 * Distance unit options
 */
export type DistanceUnit = 'miles' | 'km' | 'meters';

/**
 * Workout exercise interface
 */
export interface WorkoutExercise {
  id: string;
  workout_id: string;
  exercise_name: string;
  exercise_type?: string;
  sets?: number;
  reps?: number;
  weight?: number;
  weight_unit: WeightUnit;
  distance?: number;
  distance_unit?: DistanceUnit;
  duration_seconds?: number;
  rest_seconds?: number;
  notes?: string;
  order_index: number;
  created_at: string;
}

/**
 * Workout interface
 */
export interface Workout {
  id: string;
  user_id: string;
  workout_date: string; // ISO date string
  workout_time?: string; // Time string
  workout_type: string;
  workout_name?: string;
  duration_minutes?: number;
  calories_burned?: number;
  intensity?: WorkoutIntensity;
  location?: string;
  notes?: string;
  mood_before?: string;
  mood_after?: string;
  exercises: WorkoutExercise[];
  created_at: string;
  updated_at?: string;
}

/**
 * Request types
 */
export interface CreateWorkoutExerciseRequest {
  exercise_name: string;
  exercise_type?: string;
  sets?: number;
  reps?: number;
  weight?: number;
  weight_unit?: WeightUnit;
  distance?: number;
  distance_unit?: DistanceUnit;
  duration_seconds?: number;
  rest_seconds?: number;
  notes?: string;
  order_index?: number;
}

export interface CreateWorkoutRequest {
  workout_date: string;
  workout_time?: string;
  workout_type: string;
  workout_name?: string;
  duration_minutes?: number;
  calories_burned?: number;
  intensity?: WorkoutIntensity;
  location?: string;
  notes?: string;
  mood_before?: string;
  mood_after?: string;
  exercises?: CreateWorkoutExerciseRequest[];
}

export interface UpdateWorkoutRequest {
  workout_time?: string;
  workout_type?: string;
  workout_name?: string;
  duration_minutes?: number;
  calories_burned?: number;
  intensity?: WorkoutIntensity;
  location?: string;
  notes?: string;
  mood_before?: string;
  mood_after?: string;
}

/**
 * Workout statistics
 */
export interface WorkoutStats {
  total_workouts: number;
  total_duration: number;
  total_calories: number;
  average_intensity: string;
  most_common_type: string;
}
