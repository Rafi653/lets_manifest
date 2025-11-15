# Let's Manifest - Database Schema Design

## Overview

This document describes the complete database schema for the Let's Manifest application, supporting goals, habits, food tracking, workouts, daily reviews, blog entries, and long-term progress tracking.

## Entity Relationship Diagram

```
                                    ┌──────────────┐
                                    │    users     │
                                    ├──────────────┤
                                    │ id (PK)      │
                                    │ email        │
                                    │ username     │
                                    │ password     │
                                    │ created_at   │
                                    └──────┬───────┘
                                           │
                    ┌──────────────────────┼────────────────────────┐
                    │                      │                        │
         ┌──────────▼──────────┐  ┌───────▼────────┐  ┌───────────▼──────────┐
         │       goals         │  │     habits     │  │    daily_reviews     │
         ├─────────────────────┤  ├────────────────┤  ├──────────────────────┤
         │ id (PK)            │  │ id (PK)        │  │ id (PK)              │
         │ user_id (FK)       │  │ user_id (FK)   │  │ user_id (FK)         │
         │ title              │  │ name           │  │ review_date          │
         │ description        │  │ frequency      │  │ mood_rating          │
         │ goal_type          │  │ target_days    │  │ energy_level         │
         │ target_value       │  │ created_at     │  │ accomplishments      │
         │ start_date         │  └────────┬───────┘  │ challenges           │
         │ end_date           │           │          │ gratitude            │
         │ status             │  ┌────────▼────────┐ │ tomorrow_intentions  │
         └────────┬────────────┘  │ habit_entries  │ └──────────────────────┘
                  │               ├────────────────┤
         ┌────────▼────────┐     │ id (PK)        │  ┌──────────────────────┐
         │  goal_progress  │     │ habit_id (FK)  │  │    blog_entries      │
         ├─────────────────┤     │ entry_date     │  ├──────────────────────┤
         │ id (PK)         │     │ completed      │  │ id (PK)              │
         │ goal_id (FK)    │     │ notes          │  │ user_id (FK)         │
         │ progress_date   │     └────────────────┘  │ title                │
         │ value           │                          │ content              │
         │ notes           │                          │ status               │
         └─────────────────┘     ┌──────────────────┐ │ published_at         │
                                 │      foods       │ └──────────┬───────────┘
         ┌──────────────────┐   ├──────────────────┤            │
         │     workouts     │   │ id (PK)          │   ┌────────▼────────┐
         ├──────────────────┤   │ user_id (FK)     │   │      tags       │
         │ id (PK)          │   │ meal_type        │   ├─────────────────┤
         │ user_id (FK)     │   │ food_name        │   │ id (PK)         │
         │ workout_date     │   │ calories         │   │ name            │
         │ workout_type     │   │ protein          │   │ category        │
         │ duration_minutes │   │ carbs            │   └─────────┬───────┘
         │ calories_burned  │   │ fats             │             │
         │ notes            │   │ meal_date        │   ┌─────────▼───────┐
         └──────────┬───────┘   │ notes            │   │  taggables      │
                    │            └──────────────────┘   ├─────────────────┤
         ┌──────────▼───────┐                          │ id (PK)         │
         │ workout_exercises│                          │ tag_id (FK)     │
         ├──────────────────┤                          │ taggable_id     │
         │ id (PK)          │   ┌──────────────────┐   │ taggable_type   │
         │ workout_id (FK)  │   │      media       │   └─────────────────┘
         │ exercise_name    │   ├──────────────────┤
         │ sets             │   │ id (PK)          │
         │ reps             │   │ user_id (FK)     │
         │ weight           │   │ file_name        │
         │ notes            │   │ file_path        │
         └──────────────────┘   │ file_type        │
                                │ file_size        │
                                │ related_to_type  │
                                │ related_to_id    │
                                │ uploaded_at      │
                                └──────────────────┘
```

## Core Tables

### 1. users

Core user table for authentication and profile.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique user identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User's email address |
| username | VARCHAR(100) | UNIQUE, NOT NULL | User's username |
| password_hash | VARCHAR(255) | NOT NULL | Bcrypt hashed password |
| first_name | VARCHAR(100) | | User's first name |
| last_name | VARCHAR(100) | | User's last name |
| avatar_url | VARCHAR(500) | | Profile picture URL |
| bio | TEXT | | User biography |
| timezone | VARCHAR(50) | DEFAULT 'UTC' | User's timezone |
| is_active | BOOLEAN | DEFAULT TRUE | Account active status |
| is_verified | BOOLEAN | DEFAULT FALSE | Email verification status |
| email_verified_at | TIMESTAMP | | Email verification timestamp |
| last_login_at | TIMESTAMP | | Last login timestamp |
| created_at | TIMESTAMP | DEFAULT NOW() | Account creation timestamp |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last update timestamp |

**Indexes:**
- `idx_users_email` on (email)
- `idx_users_username` on (username)
- `idx_users_is_active` on (is_active)

---

### 2. goals

Goal tracking for daily, weekly, and monthly goals.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique goal identifier |
| user_id | UUID | FOREIGN KEY (users.id), NOT NULL | Goal owner |
| title | VARCHAR(255) | NOT NULL | Goal title |
| description | TEXT | | Detailed goal description |
| goal_type | VARCHAR(20) | NOT NULL | 'daily', 'weekly', 'monthly', 'yearly' |
| category | VARCHAR(50) | | Category (e.g., 'health', 'career', 'personal') |
| target_value | DECIMAL(10,2) | | Numeric target value |
| target_unit | VARCHAR(50) | | Unit of measurement |
| current_value | DECIMAL(10,2) | DEFAULT 0 | Current progress value |
| start_date | DATE | NOT NULL | Goal start date |
| end_date | DATE | NOT NULL | Goal end date |
| status | VARCHAR(20) | DEFAULT 'active' | 'active', 'completed', 'cancelled', 'paused' |
| priority | INTEGER | DEFAULT 0 | Priority level (0-5) |
| is_recurring | BOOLEAN | DEFAULT FALSE | Whether goal repeats |
| recurrence_pattern | VARCHAR(50) | | Recurrence pattern if recurring |
| parent_goal_id | UUID | FOREIGN KEY (goals.id) | Parent goal for sub-goals |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last update timestamp |
| completed_at | TIMESTAMP | | Completion timestamp |

**Indexes:**
- `idx_goals_user_id` on (user_id)
- `idx_goals_user_status` on (user_id, status)
- `idx_goals_user_dates` on (user_id, start_date, end_date)
- `idx_goals_goal_type` on (goal_type)
- `idx_goals_parent` on (parent_goal_id)

---

### 3. goal_progress

Track progress updates for goals.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique progress entry identifier |
| goal_id | UUID | FOREIGN KEY (goals.id), NOT NULL | Associated goal |
| progress_date | DATE | NOT NULL | Date of progress entry |
| value | DECIMAL(10,2) | NOT NULL | Progress value |
| percentage | DECIMAL(5,2) | | Progress percentage |
| notes | TEXT | | Progress notes |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |

**Indexes:**
- `idx_goal_progress_goal_id` on (goal_id)
- `idx_goal_progress_date` on (goal_id, progress_date)

---

### 4. habits

Habit tracking with streak support.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique habit identifier |
| user_id | UUID | FOREIGN KEY (users.id), NOT NULL | Habit owner |
| name | VARCHAR(255) | NOT NULL | Habit name |
| description | TEXT | | Habit description |
| frequency | VARCHAR(20) | NOT NULL | 'daily', 'weekly', 'custom' |
| target_days | INTEGER | | Target days per period |
| category | VARCHAR(50) | | Category (e.g., 'health', 'productivity') |
| color | VARCHAR(7) | | Color code for UI |
| icon | VARCHAR(50) | | Icon identifier |
| reminder_time | TIME | | Reminder time |
| is_active | BOOLEAN | DEFAULT TRUE | Whether habit is active |
| current_streak | INTEGER | DEFAULT 0 | Current consecutive days |
| longest_streak | INTEGER | DEFAULT 0 | Longest streak achieved |
| total_completions | INTEGER | DEFAULT 0 | Total times completed |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last update timestamp |

**Indexes:**
- `idx_habits_user_id` on (user_id)
- `idx_habits_user_active` on (user_id, is_active)
- `idx_habits_frequency` on (frequency)

---

### 5. habit_entries

Daily habit completion tracking.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique entry identifier |
| habit_id | UUID | FOREIGN KEY (habits.id), NOT NULL | Associated habit |
| entry_date | DATE | NOT NULL | Date of entry |
| completed | BOOLEAN | DEFAULT FALSE | Completion status |
| completed_at | TIMESTAMP | | Completion timestamp |
| notes | TEXT | | Entry notes |
| mood | VARCHAR(20) | | User mood during entry |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last update timestamp |

**Indexes:**
- `idx_habit_entries_habit_id` on (habit_id)
- `idx_habit_entries_date` on (habit_id, entry_date)
- `idx_habit_entries_completed` on (habit_id, completed, entry_date)

**Constraints:**
- UNIQUE (habit_id, entry_date)

---

### 6. foods

Food tracking and nutrition logging.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique food entry identifier |
| user_id | UUID | FOREIGN KEY (users.id), NOT NULL | Food entry owner |
| meal_date | DATE | NOT NULL | Date of meal |
| meal_time | TIME | | Time of meal |
| meal_type | VARCHAR(20) | NOT NULL | 'breakfast', 'lunch', 'dinner', 'snack' |
| food_name | VARCHAR(255) | NOT NULL | Name of food item |
| portion_size | VARCHAR(100) | | Portion size description |
| calories | DECIMAL(8,2) | | Calories |
| protein_grams | DECIMAL(6,2) | | Protein in grams |
| carbs_grams | DECIMAL(6,2) | | Carbohydrates in grams |
| fats_grams | DECIMAL(6,2) | | Fats in grams |
| fiber_grams | DECIMAL(6,2) | | Fiber in grams |
| sugar_grams | DECIMAL(6,2) | | Sugar in grams |
| sodium_mg | DECIMAL(8,2) | | Sodium in milligrams |
| notes | TEXT | | Additional notes |
| is_favorite | BOOLEAN | DEFAULT FALSE | Mark as favorite food |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last update timestamp |

**Indexes:**
- `idx_foods_user_id` on (user_id)
- `idx_foods_user_date` on (user_id, meal_date)
- `idx_foods_meal_type` on (user_id, meal_type)
- `idx_foods_favorites` on (user_id, is_favorite)

---

### 7. workouts

Workout tracking and exercise logs.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique workout identifier |
| user_id | UUID | FOREIGN KEY (users.id), NOT NULL | Workout owner |
| workout_date | DATE | NOT NULL | Date of workout |
| workout_time | TIME | | Time of workout |
| workout_type | VARCHAR(50) | NOT NULL | Type (e.g., 'strength', 'cardio', 'yoga') |
| workout_name | VARCHAR(255) | | Name/title of workout |
| duration_minutes | INTEGER | | Duration in minutes |
| calories_burned | DECIMAL(8,2) | | Estimated calories burned |
| intensity | VARCHAR(20) | | 'low', 'medium', 'high' |
| location | VARCHAR(100) | | Workout location |
| notes | TEXT | | Workout notes |
| mood_before | VARCHAR(20) | | Mood before workout |
| mood_after | VARCHAR(20) | | Mood after workout |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last update timestamp |

**Indexes:**
- `idx_workouts_user_id` on (user_id)
- `idx_workouts_user_date` on (user_id, workout_date)
- `idx_workouts_type` on (user_id, workout_type)

---

### 8. workout_exercises

Individual exercises within a workout.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique exercise identifier |
| workout_id | UUID | FOREIGN KEY (workouts.id), NOT NULL | Associated workout |
| exercise_name | VARCHAR(255) | NOT NULL | Name of exercise |
| exercise_type | VARCHAR(50) | | Type (e.g., 'barbell', 'dumbbell', 'bodyweight') |
| sets | INTEGER | | Number of sets |
| reps | INTEGER | | Repetitions per set |
| weight | DECIMAL(6,2) | | Weight used |
| weight_unit | VARCHAR(10) | DEFAULT 'lbs' | 'lbs', 'kg' |
| distance | DECIMAL(8,2) | | Distance (for cardio) |
| distance_unit | VARCHAR(10) | | 'miles', 'km', 'meters' |
| duration_seconds | INTEGER | | Duration for timed exercises |
| rest_seconds | INTEGER | | Rest between sets |
| notes | TEXT | | Exercise notes |
| order_index | INTEGER | DEFAULT 0 | Order in workout |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |

**Indexes:**
- `idx_workout_exercises_workout_id` on (workout_id)
- `idx_workout_exercises_order` on (workout_id, order_index)

---

### 9. daily_reviews

End-of-day reflection and review.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique review identifier |
| user_id | UUID | FOREIGN KEY (users.id), NOT NULL | Review owner |
| review_date | DATE | NOT NULL | Date of review |
| mood_rating | INTEGER | CHECK (mood_rating >= 1 AND mood_rating <= 10) | Overall mood (1-10) |
| energy_level | INTEGER | CHECK (energy_level >= 1 AND energy_level <= 10) | Energy level (1-10) |
| productivity_rating | INTEGER | CHECK (productivity_rating >= 1 AND productivity_rating <= 10) | Productivity (1-10) |
| sleep_hours | DECIMAL(3,1) | | Hours of sleep |
| sleep_quality | INTEGER | CHECK (sleep_quality >= 1 AND sleep_quality <= 10) | Sleep quality (1-10) |
| water_intake_ml | INTEGER | | Water intake in milliliters |
| accomplishments | TEXT | | What was accomplished |
| challenges | TEXT | | Challenges faced |
| lessons_learned | TEXT | | Lessons learned |
| gratitude | TEXT | | Things to be grateful for |
| tomorrow_intentions | TEXT | | Intentions for tomorrow |
| highlights | TEXT | | Day highlights |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last update timestamp |

**Indexes:**
- `idx_daily_reviews_user_id` on (user_id)
- `idx_daily_reviews_date` on (user_id, review_date)

**Constraints:**
- UNIQUE (user_id, review_date)

---

### 10. blog_entries

Blog posts and journal entries.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique blog entry identifier |
| user_id | UUID | FOREIGN KEY (users.id), NOT NULL | Entry owner |
| title | VARCHAR(500) | NOT NULL | Entry title |
| content | TEXT | NOT NULL | Entry content (Markdown supported) |
| excerpt | TEXT | | Short excerpt/summary |
| slug | VARCHAR(500) | UNIQUE | URL-friendly slug |
| status | VARCHAR(20) | DEFAULT 'draft' | 'draft', 'published', 'archived' |
| is_public | BOOLEAN | DEFAULT FALSE | Public visibility |
| is_featured | BOOLEAN | DEFAULT FALSE | Featured status |
| view_count | INTEGER | DEFAULT 0 | Number of views |
| published_at | TIMESTAMP | | Publication timestamp |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last update timestamp |

**Indexes:**
- `idx_blog_entries_user_id` on (user_id)
- `idx_blog_entries_status` on (status, published_at)
- `idx_blog_entries_slug` on (slug)
- `idx_blog_entries_public` on (is_public, published_at)

---

### 11. tags

Tagging system for categorization.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique tag identifier |
| name | VARCHAR(50) | NOT NULL | Tag name |
| slug | VARCHAR(50) | UNIQUE, NOT NULL | URL-friendly slug |
| category | VARCHAR(50) | | Tag category |
| color | VARCHAR(7) | | Color code |
| description | TEXT | | Tag description |
| usage_count | INTEGER | DEFAULT 0 | Times used |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |

**Indexes:**
- `idx_tags_name` on (name)
- `idx_tags_slug` on (slug)
- `idx_tags_category` on (category)

---

### 12. taggables

Polymorphic association table for tags.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique association identifier |
| tag_id | UUID | FOREIGN KEY (tags.id), NOT NULL | Associated tag |
| taggable_id | UUID | NOT NULL | Tagged entity ID |
| taggable_type | VARCHAR(50) | NOT NULL | Entity type ('goal', 'habit', 'blog_entry', etc.) |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |

**Indexes:**
- `idx_taggables_tag_id` on (tag_id)
- `idx_taggables_polymorphic` on (taggable_type, taggable_id)

**Constraints:**
- UNIQUE (tag_id, taggable_type, taggable_id)

---

### 13. media

File uploads and media management.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique media identifier |
| user_id | UUID | FOREIGN KEY (users.id), NOT NULL | Media owner |
| file_name | VARCHAR(255) | NOT NULL | Original filename |
| file_path | VARCHAR(1000) | NOT NULL | Storage path/URL |
| file_type | VARCHAR(100) | NOT NULL | MIME type |
| file_size | BIGINT | NOT NULL | File size in bytes |
| width | INTEGER | | Image width (if applicable) |
| height | INTEGER | | Image height (if applicable) |
| alt_text | VARCHAR(255) | | Alt text for accessibility |
| related_to_type | VARCHAR(50) | | Related entity type |
| related_to_id | UUID | | Related entity ID |
| is_public | BOOLEAN | DEFAULT FALSE | Public accessibility |
| uploaded_at | TIMESTAMP | DEFAULT NOW() | Upload timestamp |

**Indexes:**
- `idx_media_user_id` on (user_id)
- `idx_media_related` on (related_to_type, related_to_id)
- `idx_media_file_type` on (file_type)

---

### 14. progress_snapshots

Long-term progress tracking across all modules.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique snapshot identifier |
| user_id | UUID | FOREIGN KEY (users.id), NOT NULL | Snapshot owner |
| snapshot_date | DATE | NOT NULL | Snapshot date |
| snapshot_type | VARCHAR(50) | NOT NULL | Type (e.g., 'weekly', 'monthly', 'yearly') |
| total_goals | INTEGER | DEFAULT 0 | Total goals |
| completed_goals | INTEGER | DEFAULT 0 | Completed goals |
| active_habits | INTEGER | DEFAULT 0 | Active habits tracked |
| habit_completion_rate | DECIMAL(5,2) | | Habit completion percentage |
| total_workouts | INTEGER | DEFAULT 0 | Total workouts |
| total_workout_minutes | INTEGER | DEFAULT 0 | Total workout duration |
| average_daily_mood | DECIMAL(3,1) | | Average mood rating |
| average_energy_level | DECIMAL(3,1) | | Average energy level |
| total_blog_entries | INTEGER | DEFAULT 0 | Total blog entries |
| weight | DECIMAL(5,2) | | Body weight |
| weight_unit | VARCHAR(10) | DEFAULT 'lbs' | Weight unit |
| body_fat_percentage | DECIMAL(4,2) | | Body fat percentage |
| notes | TEXT | | Additional notes |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |

**Indexes:**
- `idx_progress_snapshots_user_id` on (user_id)
- `idx_progress_snapshots_date` on (user_id, snapshot_date)
- `idx_progress_snapshots_type` on (user_id, snapshot_type)

**Constraints:**
- UNIQUE (user_id, snapshot_date, snapshot_type)

---

## Relationships Summary

### One-to-Many Relationships
- users → goals (one user has many goals)
- users → habits (one user has many habits)
- users → foods (one user has many food entries)
- users → workouts (one user has many workouts)
- users → daily_reviews (one user has many reviews)
- users → blog_entries (one user has many blog entries)
- users → media (one user has many media files)
- users → progress_snapshots (one user has many snapshots)
- goals → goal_progress (one goal has many progress entries)
- habits → habit_entries (one habit has many entries)
- workouts → workout_exercises (one workout has many exercises)

### Self-Referential
- goals → goals (parent_goal_id for sub-goals)

### Many-to-Many (via taggables)
- tags ↔ goals
- tags ↔ habits
- tags ↔ blog_entries
- tags ↔ workouts

### Polymorphic
- media → * (can relate to any entity)
- taggables → * (can tag any entity)

---

## Key Features & Query Patterns

### 1. Goal Tracking Queries
```sql
-- Get active goals for a user
SELECT * FROM goals 
WHERE user_id = ? AND status = 'active' 
ORDER BY priority DESC, end_date ASC;

-- Get goal progress history
SELECT gp.*, g.title 
FROM goal_progress gp
JOIN goals g ON gp.goal_id = g.id
WHERE g.user_id = ? AND g.id = ?
ORDER BY gp.progress_date DESC;

-- Get goals by type and date range
SELECT * FROM goals
WHERE user_id = ? 
  AND goal_type = ?
  AND start_date >= ? AND end_date <= ?;
```

### 2. Habit Streak Queries
```sql
-- Get habit streak information
SELECT h.*, COUNT(he.id) as total_entries,
       SUM(CASE WHEN he.completed THEN 1 ELSE 0 END) as completed_count
FROM habits h
LEFT JOIN habit_entries he ON h.id = he.habit_id
WHERE h.user_id = ? AND h.is_active = true
GROUP BY h.id;

-- Get habit entries for a date range
SELECT * FROM habit_entries
WHERE habit_id = ? 
  AND entry_date >= ? AND entry_date <= ?
ORDER BY entry_date DESC;

-- Check if habit was completed today
SELECT completed FROM habit_entries
WHERE habit_id = ? AND entry_date = CURRENT_DATE;
```

### 3. Food Tracking Queries
```sql
-- Get daily nutrition summary
SELECT meal_date,
       SUM(calories) as total_calories,
       SUM(protein_grams) as total_protein,
       SUM(carbs_grams) as total_carbs,
       SUM(fats_grams) as total_fats
FROM foods
WHERE user_id = ? AND meal_date = ?
GROUP BY meal_date;

-- Get foods by meal type
SELECT * FROM foods
WHERE user_id = ? AND meal_date = ? AND meal_type = ?
ORDER BY meal_time;
```

### 4. Workout Tracking Queries
```sql
-- Get workouts with exercises
SELECT w.*, 
       json_agg(we.*) as exercises
FROM workouts w
LEFT JOIN workout_exercises we ON w.id = we.workout_id
WHERE w.user_id = ?
GROUP BY w.id
ORDER BY w.workout_date DESC;

-- Get workout statistics
SELECT workout_type,
       COUNT(*) as workout_count,
       SUM(duration_minutes) as total_minutes,
       AVG(calories_burned) as avg_calories
FROM workouts
WHERE user_id = ? 
  AND workout_date >= ? AND workout_date <= ?
GROUP BY workout_type;
```

### 5. Daily Review Queries
```sql
-- Get daily review
SELECT * FROM daily_reviews
WHERE user_id = ? AND review_date = ?;

-- Get review trends
SELECT 
    DATE_TRUNC('week', review_date) as week,
    AVG(mood_rating) as avg_mood,
    AVG(energy_level) as avg_energy,
    AVG(productivity_rating) as avg_productivity
FROM daily_reviews
WHERE user_id = ? 
  AND review_date >= ? AND review_date <= ?
GROUP BY week
ORDER BY week;
```

### 6. Blog Entry Queries
```sql
-- Get published blog entries
SELECT * FROM blog_entries
WHERE user_id = ? AND status = 'published'
ORDER BY published_at DESC;

-- Get blog entries with tags
SELECT be.*, 
       json_agg(t.*) as tags
FROM blog_entries be
LEFT JOIN taggables tg ON tg.taggable_id = be.id AND tg.taggable_type = 'blog_entry'
LEFT JOIN tags t ON tg.tag_id = t.id
WHERE be.user_id = ?
GROUP BY be.id
ORDER BY be.published_at DESC;
```

### 7. Progress Snapshot Queries
```sql
-- Get latest progress snapshot
SELECT * FROM progress_snapshots
WHERE user_id = ? 
ORDER BY snapshot_date DESC
LIMIT 1;

-- Compare progress over time
SELECT snapshot_date,
       completed_goals,
       habit_completion_rate,
       average_daily_mood,
       total_workouts
FROM progress_snapshots
WHERE user_id = ? AND snapshot_type = 'weekly'
ORDER BY snapshot_date DESC
LIMIT 12;
```

---

## Performance Considerations

### Indexing Strategy
1. **Primary Keys**: All tables have UUID primary keys
2. **Foreign Keys**: Indexed for join performance
3. **Common Filters**: user_id, dates, status fields
4. **Composite Indexes**: For multi-column queries
5. **Unique Constraints**: Prevent duplicates

### Query Optimization
1. Use appropriate indexes for filtering and sorting
2. Limit result sets with pagination
3. Use aggregations in database rather than application
4. Consider materialized views for complex analytics
5. Use connection pooling

### Data Partitioning (Future)
For large datasets, consider partitioning:
- foods, workouts, habit_entries by date (monthly/yearly)
- blog_entries by published_at
- progress_snapshots by snapshot_date

---

## Data Integrity

### Foreign Key Constraints
- All foreign keys have ON DELETE CASCADE or ON DELETE SET NULL
- Ensures referential integrity

### Check Constraints
- Rating fields limited to 1-10 range
- Status fields use ENUM-like constraints
- Numeric fields have appropriate precision

### Default Values
- Timestamps default to NOW()
- Boolean flags have sensible defaults
- Counters default to 0

---

## Security Considerations

1. **Password Storage**: Use bcrypt with appropriate cost factor
2. **Input Validation**: Validate all inputs at application layer
3. **SQL Injection**: Use parameterized queries (ORM handles this)
4. **Access Control**: Enforce user_id checks at service layer
5. **Data Privacy**: Encrypt sensitive fields if needed
6. **Audit Trail**: Timestamps on all tables

---

## Migration Strategy

1. **Phase 1**: Core tables (users, tags, media)
2. **Phase 2**: Goals and progress tracking
3. **Phase 3**: Habits and daily reviews
4. **Phase 4**: Food and workout tracking
5. **Phase 5**: Blog entries and advanced features

Each phase should include:
- Migration scripts (up and down)
- Seed data for testing
- Updated API endpoints
- Frontend integration

---

## Future Enhancements

1. **Social Features**
   - User follows/followers
   - Shared goals and challenges
   - Activity feeds

2. **Analytics Tables**
   - Aggregated statistics
   - Trend analysis
   - Materialized views

3. **Notification System**
   - Notification preferences
   - Notification history

4. **Integration Tables**
   - External service connections
   - API sync logs

5. **Advanced Features**
   - AI recommendations
   - Custom fields/attributes
   - Template system
