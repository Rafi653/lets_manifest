-- Let's Manifest Database Schema
-- PostgreSQL 15+
-- Generated: 2025-11-15

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ================================================================
-- Core Tables
-- ================================================================

-- Table: users
-- Description: Core user authentication and profile information
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    avatar_url VARCHAR(500),
    bio TEXT,
    timezone VARCHAR(50) DEFAULT 'UTC',
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    email_verified_at TIMESTAMP,
    last_login_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for users table
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_is_active ON users(is_active);

-- ================================================================
-- Goals Module
-- ================================================================

-- Table: goals
-- Description: Goal tracking for daily, weekly, monthly, and yearly goals
CREATE TABLE goals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    goal_type VARCHAR(20) NOT NULL CHECK (goal_type IN ('daily', 'weekly', 'monthly', 'yearly')),
    category VARCHAR(50),
    target_value DECIMAL(10,2),
    target_unit VARCHAR(50),
    current_value DECIMAL(10,2) DEFAULT 0,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'completed', 'cancelled', 'paused')),
    priority INTEGER DEFAULT 0 CHECK (priority >= 0 AND priority <= 5),
    is_recurring BOOLEAN DEFAULT FALSE,
    recurrence_pattern VARCHAR(50),
    parent_goal_id UUID REFERENCES goals(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- Indexes for goals table
CREATE INDEX idx_goals_user_id ON goals(user_id);
CREATE INDEX idx_goals_user_status ON goals(user_id, status);
CREATE INDEX idx_goals_user_dates ON goals(user_id, start_date, end_date);
CREATE INDEX idx_goals_goal_type ON goals(goal_type);
CREATE INDEX idx_goals_parent ON goals(parent_goal_id);

-- Table: goal_progress
-- Description: Track progress updates for goals
CREATE TABLE goal_progress (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    goal_id UUID NOT NULL REFERENCES goals(id) ON DELETE CASCADE,
    progress_date DATE NOT NULL,
    value DECIMAL(10,2) NOT NULL,
    percentage DECIMAL(5,2),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for goal_progress table
CREATE INDEX idx_goal_progress_goal_id ON goal_progress(goal_id);
CREATE INDEX idx_goal_progress_date ON goal_progress(goal_id, progress_date);

-- ================================================================
-- Habits Module
-- ================================================================

-- Table: habits
-- Description: Habit tracking with streak support
CREATE TABLE habits (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    frequency VARCHAR(20) NOT NULL CHECK (frequency IN ('daily', 'weekly', 'custom')),
    target_days INTEGER,
    category VARCHAR(50),
    color VARCHAR(7),
    icon VARCHAR(50),
    reminder_time TIME,
    is_active BOOLEAN DEFAULT TRUE,
    current_streak INTEGER DEFAULT 0,
    longest_streak INTEGER DEFAULT 0,
    total_completions INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for habits table
CREATE INDEX idx_habits_user_id ON habits(user_id);
CREATE INDEX idx_habits_user_active ON habits(user_id, is_active);
CREATE INDEX idx_habits_frequency ON habits(frequency);

-- Table: habit_entries
-- Description: Daily habit completion tracking
CREATE TABLE habit_entries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    habit_id UUID NOT NULL REFERENCES habits(id) ON DELETE CASCADE,
    entry_date DATE NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP,
    notes TEXT,
    mood VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(habit_id, entry_date)
);

-- Indexes for habit_entries table
CREATE INDEX idx_habit_entries_habit_id ON habit_entries(habit_id);
CREATE INDEX idx_habit_entries_date ON habit_entries(habit_id, entry_date);
CREATE INDEX idx_habit_entries_completed ON habit_entries(habit_id, completed, entry_date);

-- ================================================================
-- Food Tracking Module
-- ================================================================

-- Table: foods
-- Description: Food tracking and nutrition logging
CREATE TABLE foods (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    meal_date DATE NOT NULL,
    meal_time TIME,
    meal_type VARCHAR(20) NOT NULL CHECK (meal_type IN ('breakfast', 'lunch', 'dinner', 'snack')),
    food_name VARCHAR(255) NOT NULL,
    portion_size VARCHAR(100),
    calories DECIMAL(8,2),
    protein_grams DECIMAL(6,2),
    carbs_grams DECIMAL(6,2),
    fats_grams DECIMAL(6,2),
    fiber_grams DECIMAL(6,2),
    sugar_grams DECIMAL(6,2),
    sodium_mg DECIMAL(8,2),
    notes TEXT,
    is_favorite BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for foods table
CREATE INDEX idx_foods_user_id ON foods(user_id);
CREATE INDEX idx_foods_user_date ON foods(user_id, meal_date);
CREATE INDEX idx_foods_meal_type ON foods(user_id, meal_type);
CREATE INDEX idx_foods_favorites ON foods(user_id, is_favorite);

-- ================================================================
-- Workout Tracking Module
-- ================================================================

-- Table: workouts
-- Description: Workout tracking and exercise logs
CREATE TABLE workouts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    workout_date DATE NOT NULL,
    workout_time TIME,
    workout_type VARCHAR(50) NOT NULL,
    workout_name VARCHAR(255),
    duration_minutes INTEGER,
    calories_burned DECIMAL(8,2),
    intensity VARCHAR(20) CHECK (intensity IN ('low', 'medium', 'high')),
    location VARCHAR(100),
    notes TEXT,
    mood_before VARCHAR(20),
    mood_after VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for workouts table
CREATE INDEX idx_workouts_user_id ON workouts(user_id);
CREATE INDEX idx_workouts_user_date ON workouts(user_id, workout_date);
CREATE INDEX idx_workouts_type ON workouts(user_id, workout_type);

-- Table: workout_exercises
-- Description: Individual exercises within a workout
CREATE TABLE workout_exercises (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workout_id UUID NOT NULL REFERENCES workouts(id) ON DELETE CASCADE,
    exercise_name VARCHAR(255) NOT NULL,
    exercise_type VARCHAR(50),
    sets INTEGER,
    reps INTEGER,
    weight DECIMAL(6,2),
    weight_unit VARCHAR(10) DEFAULT 'lbs' CHECK (weight_unit IN ('lbs', 'kg')),
    distance DECIMAL(8,2),
    distance_unit VARCHAR(10) CHECK (distance_unit IN ('miles', 'km', 'meters')),
    duration_seconds INTEGER,
    rest_seconds INTEGER,
    notes TEXT,
    order_index INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for workout_exercises table
CREATE INDEX idx_workout_exercises_workout_id ON workout_exercises(workout_id);
CREATE INDEX idx_workout_exercises_order ON workout_exercises(workout_id, order_index);

-- ================================================================
-- Daily Reviews Module
-- ================================================================

-- Table: daily_reviews
-- Description: End-of-day reflection and review
CREATE TABLE daily_reviews (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    review_date DATE NOT NULL,
    mood_rating INTEGER CHECK (mood_rating >= 1 AND mood_rating <= 10),
    energy_level INTEGER CHECK (energy_level >= 1 AND energy_level <= 10),
    productivity_rating INTEGER CHECK (productivity_rating >= 1 AND productivity_rating <= 10),
    sleep_hours DECIMAL(3,1),
    sleep_quality INTEGER CHECK (sleep_quality >= 1 AND sleep_quality <= 10),
    water_intake_ml INTEGER,
    accomplishments TEXT,
    challenges TEXT,
    lessons_learned TEXT,
    gratitude TEXT,
    tomorrow_intentions TEXT,
    highlights TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, review_date)
);

-- Indexes for daily_reviews table
CREATE INDEX idx_daily_reviews_user_id ON daily_reviews(user_id);
CREATE INDEX idx_daily_reviews_date ON daily_reviews(user_id, review_date);

-- ================================================================
-- Blog Entries Module
-- ================================================================

-- Table: blog_entries
-- Description: Blog posts and journal entries
CREATE TABLE blog_entries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    excerpt TEXT,
    slug VARCHAR(500) UNIQUE,
    status VARCHAR(20) DEFAULT 'draft' CHECK (status IN ('draft', 'published', 'archived')),
    is_public BOOLEAN DEFAULT FALSE,
    is_featured BOOLEAN DEFAULT FALSE,
    view_count INTEGER DEFAULT 0,
    published_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for blog_entries table
CREATE INDEX idx_blog_entries_user_id ON blog_entries(user_id);
CREATE INDEX idx_blog_entries_status ON blog_entries(status, published_at);
CREATE INDEX idx_blog_entries_slug ON blog_entries(slug);
CREATE INDEX idx_blog_entries_public ON blog_entries(is_public, published_at);

-- ================================================================
-- Supporting Tables
-- ================================================================

-- Table: tags
-- Description: Tagging system for categorization
CREATE TABLE tags (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(50) NOT NULL,
    slug VARCHAR(50) UNIQUE NOT NULL,
    category VARCHAR(50),
    color VARCHAR(7),
    description TEXT,
    usage_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for tags table
CREATE INDEX idx_tags_name ON tags(name);
CREATE INDEX idx_tags_slug ON tags(slug);
CREATE INDEX idx_tags_category ON tags(category);

-- Table: taggables
-- Description: Polymorphic association table for tags
CREATE TABLE taggables (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tag_id UUID NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    taggable_id UUID NOT NULL,
    taggable_type VARCHAR(50) NOT NULL CHECK (taggable_type IN ('goal', 'habit', 'blog_entry', 'workout', 'food', 'daily_review')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(tag_id, taggable_type, taggable_id)
);

-- Indexes for taggables table
CREATE INDEX idx_taggables_tag_id ON taggables(tag_id);
CREATE INDEX idx_taggables_polymorphic ON taggables(taggable_type, taggable_id);

-- Table: media
-- Description: File uploads and media management
CREATE TABLE media (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(1000) NOT NULL,
    file_type VARCHAR(100) NOT NULL,
    file_size BIGINT NOT NULL,
    width INTEGER,
    height INTEGER,
    alt_text VARCHAR(255),
    related_to_type VARCHAR(50),
    related_to_id UUID,
    is_public BOOLEAN DEFAULT FALSE,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for media table
CREATE INDEX idx_media_user_id ON media(user_id);
CREATE INDEX idx_media_related ON media(related_to_type, related_to_id);
CREATE INDEX idx_media_file_type ON media(file_type);

-- Table: progress_snapshots
-- Description: Long-term progress tracking across all modules
CREATE TABLE progress_snapshots (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    snapshot_date DATE NOT NULL,
    snapshot_type VARCHAR(50) NOT NULL CHECK (snapshot_type IN ('weekly', 'monthly', 'yearly')),
    total_goals INTEGER DEFAULT 0,
    completed_goals INTEGER DEFAULT 0,
    active_habits INTEGER DEFAULT 0,
    habit_completion_rate DECIMAL(5,2),
    total_workouts INTEGER DEFAULT 0,
    total_workout_minutes INTEGER DEFAULT 0,
    average_daily_mood DECIMAL(3,1),
    average_energy_level DECIMAL(3,1),
    total_blog_entries INTEGER DEFAULT 0,
    weight DECIMAL(5,2),
    weight_unit VARCHAR(10) DEFAULT 'lbs' CHECK (weight_unit IN ('lbs', 'kg')),
    body_fat_percentage DECIMAL(4,2),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, snapshot_date, snapshot_type)
);

-- Indexes for progress_snapshots table
CREATE INDEX idx_progress_snapshots_user_id ON progress_snapshots(user_id);
CREATE INDEX idx_progress_snapshots_date ON progress_snapshots(user_id, snapshot_date);
CREATE INDEX idx_progress_snapshots_type ON progress_snapshots(user_id, snapshot_type);

-- ================================================================
-- Triggers for updated_at timestamps
-- ================================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply trigger to tables with updated_at column
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_goals_updated_at BEFORE UPDATE ON goals
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_habits_updated_at BEFORE UPDATE ON habits
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_habit_entries_updated_at BEFORE UPDATE ON habit_entries
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_foods_updated_at BEFORE UPDATE ON foods
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_workouts_updated_at BEFORE UPDATE ON workouts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_daily_reviews_updated_at BEFORE UPDATE ON daily_reviews
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_blog_entries_updated_at BEFORE UPDATE ON blog_entries
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ================================================================
-- Comments for documentation
-- ================================================================

COMMENT ON TABLE users IS 'Core user authentication and profile information';
COMMENT ON TABLE goals IS 'Goal tracking for daily, weekly, monthly, and yearly goals';
COMMENT ON TABLE goal_progress IS 'Track progress updates for goals';
COMMENT ON TABLE habits IS 'Habit tracking with streak support';
COMMENT ON TABLE habit_entries IS 'Daily habit completion tracking';
COMMENT ON TABLE foods IS 'Food tracking and nutrition logging';
COMMENT ON TABLE workouts IS 'Workout tracking and exercise logs';
COMMENT ON TABLE workout_exercises IS 'Individual exercises within a workout';
COMMENT ON TABLE daily_reviews IS 'End-of-day reflection and review';
COMMENT ON TABLE blog_entries IS 'Blog posts and journal entries';
COMMENT ON TABLE tags IS 'Tagging system for categorization';
COMMENT ON TABLE taggables IS 'Polymorphic association table for tags';
COMMENT ON TABLE media IS 'File uploads and media management';
COMMENT ON TABLE progress_snapshots IS 'Long-term progress tracking across all modules';
