# Database Schema Quick Reference

## Tables Overview

| Table | Purpose | Key Fields | Relationships |
|-------|---------|------------|---------------|
| **users** | User authentication & profile | email, username, password_hash | → goals, habits, foods, workouts, etc. |
| **goals** | Goal tracking | title, goal_type, status, dates | ← user, → goal_progress |
| **goal_progress** | Goal progress entries | goal_id, progress_date, value | ← goal |
| **habits** | Habit definitions | name, frequency, streak data | ← user, → habit_entries |
| **habit_entries** | Daily habit records | habit_id, entry_date, completed | ← habit |
| **foods** | Food & nutrition logs | meal_type, nutrition data | ← user |
| **workouts** | Workout sessions | workout_type, duration, calories | ← user, → workout_exercises |
| **workout_exercises** | Individual exercises | exercise_name, sets, reps, weight | ← workout |
| **daily_reviews** | Daily reflections | review_date, ratings, reflections | ← user |
| **blog_entries** | Blog posts | title, content, status | ← user |
| **tags** | Tag definitions | name, slug, category | → taggables |
| **taggables** | Polymorphic tag links | tag_id, taggable_type, taggable_id | ← tag |
| **media** | File uploads | file_name, file_path, file_type | ← user |
| **progress_snapshots** | Aggregated metrics | snapshot_date, metrics | ← user |

---

## Common Queries Cheat Sheet

### Goals

```sql
-- Get active goals
SELECT * FROM goals WHERE user_id = ? AND status = 'active' ORDER BY priority DESC;

-- Get goal with progress
SELECT g.*, gp.progress_date, gp.value 
FROM goals g 
LEFT JOIN goal_progress gp ON g.id = gp.goal_id 
WHERE g.id = ?;

-- Get goals by type and date range
SELECT * FROM goals 
WHERE user_id = ? AND goal_type = 'weekly' 
AND start_date >= ? AND end_date <= ?;
```

### Habits

```sql
-- Get active habits with today's status
SELECT h.*, he.completed 
FROM habits h 
LEFT JOIN habit_entries he ON h.id = he.habit_id AND he.entry_date = CURRENT_DATE
WHERE h.user_id = ? AND h.is_active = true;

-- Calculate habit completion rate
SELECT h.name, 
       COUNT(he.id) as total,
       SUM(CASE WHEN he.completed THEN 1 ELSE 0 END) as completed,
       ROUND(SUM(CASE WHEN he.completed THEN 1 ELSE 0 END) * 100.0 / COUNT(he.id), 2) as rate
FROM habits h
JOIN habit_entries he ON h.id = he.habit_id
WHERE h.user_id = ? AND he.entry_date >= ?
GROUP BY h.id, h.name;

-- Get habit streak history
SELECT entry_date, completed 
FROM habit_entries 
WHERE habit_id = ? 
ORDER BY entry_date DESC 
LIMIT 30;
```

### Foods

```sql
-- Get today's meals
SELECT * FROM foods 
WHERE user_id = ? AND meal_date = CURRENT_DATE 
ORDER BY meal_time;

-- Daily nutrition summary
SELECT 
    meal_date,
    SUM(calories) as total_calories,
    SUM(protein_grams) as total_protein,
    SUM(carbs_grams) as total_carbs,
    SUM(fats_grams) as total_fats
FROM foods
WHERE user_id = ? AND meal_date = ?
GROUP BY meal_date;

-- Get favorite foods
SELECT DISTINCT food_name, AVG(calories) as avg_calories
FROM foods
WHERE user_id = ? AND is_favorite = true
GROUP BY food_name;
```

### Workouts

```sql
-- Get recent workouts with exercises
SELECT w.*, 
       json_agg(we.* ORDER BY we.order_index) as exercises
FROM workouts w
LEFT JOIN workout_exercises we ON w.id = we.workout_id
WHERE w.user_id = ?
GROUP BY w.id
ORDER BY w.workout_date DESC
LIMIT 10;

-- Workout statistics
SELECT 
    workout_type,
    COUNT(*) as count,
    SUM(duration_minutes) as total_minutes,
    AVG(calories_burned) as avg_calories
FROM workouts
WHERE user_id = ? AND workout_date >= ?
GROUP BY workout_type;

-- Exercise progress over time
SELECT 
    we.exercise_name,
    w.workout_date,
    we.weight,
    we.sets,
    we.reps
FROM workout_exercises we
JOIN workouts w ON we.workout_id = w.id
WHERE w.user_id = ? AND we.exercise_name = ?
ORDER BY w.workout_date DESC;
```

### Daily Reviews

```sql
-- Get recent reviews
SELECT * FROM daily_reviews 
WHERE user_id = ? 
ORDER BY review_date DESC 
LIMIT 30;

-- Weekly mood trends
SELECT 
    DATE_TRUNC('week', review_date) as week,
    AVG(mood_rating) as avg_mood,
    AVG(energy_level) as avg_energy,
    AVG(productivity_rating) as avg_productivity
FROM daily_reviews
WHERE user_id = ? AND review_date >= ?
GROUP BY DATE_TRUNC('week', review_date)
ORDER BY week DESC;

-- Get review by date
SELECT * FROM daily_reviews 
WHERE user_id = ? AND review_date = ?;
```

### Tags

```sql
-- Get entities by tag
SELECT t.name, tg.taggable_type, tg.taggable_id
FROM tags t
JOIN taggables tg ON t.id = tg.tag_id
WHERE t.slug = ?;

-- Get tags for entity
SELECT t.* FROM tags t
JOIN taggables tg ON t.id = tg.tag_id
WHERE tg.taggable_type = ? AND tg.taggable_id = ?;

-- Most used tags
SELECT * FROM tags 
ORDER BY usage_count DESC 
LIMIT 10;
```

### Progress Snapshots

```sql
-- Latest snapshot
SELECT * FROM progress_snapshots
WHERE user_id = ?
ORDER BY snapshot_date DESC
LIMIT 1;

-- Monthly snapshots comparison
SELECT 
    snapshot_date,
    completed_goals,
    habit_completion_rate,
    total_workouts,
    average_daily_mood
FROM progress_snapshots
WHERE user_id = ? AND snapshot_type = 'monthly'
ORDER BY snapshot_date DESC
LIMIT 12;
```

---

## SQLAlchemy Model Usage

### Import Models

```python
from app.models import (
    User, Goal, GoalProgress, Habit, HabitEntry,
    Food, Workout, WorkoutExercise, DailyReview,
    BlogEntry, Tag, Taggable, Media, ProgressSnapshot
)
```

### Common Operations

```python
# Create
goal = Goal(user_id=user.id, title="My Goal", goal_type="daily")
db.add(goal)
db.commit()

# Read
goal = db.query(Goal).filter(Goal.id == goal_id).first()
goals = db.query(Goal).filter(Goal.user_id == user_id).all()

# Update
goal.status = "completed"
goal.completed_at = datetime.utcnow()
db.commit()

# Delete
db.delete(goal)
db.commit()

# With relationships
workout = db.query(Workout).options(joinedload(Workout.exercises)).get(workout_id)
for exercise in workout.exercises:
    print(exercise.exercise_name)
```

---

## Validation Rules

### Goal Type
- Values: `daily`, `weekly`, `monthly`, `yearly`

### Goal Status
- Values: `active`, `completed`, `cancelled`, `paused`

### Habit Frequency
- Values: `daily`, `weekly`, `custom`

### Meal Type
- Values: `breakfast`, `lunch`, `dinner`, `snack`

### Workout Intensity
- Values: `low`, `medium`, `high`

### Blog Status
- Values: `draft`, `published`, `archived`

### Ratings (1-10)
- mood_rating, energy_level, productivity_rating, sleep_quality

### Priority (0-5)
- goal.priority

### Weight Unit
- Values: `lbs`, `kg`

### Distance Unit
- Values: `miles`, `km`, `meters`

---

## Indexes for Performance

### Critical Indexes
```
users: email, username, is_active
goals: user_id, (user_id, status), (user_id, start_date, end_date)
habits: user_id, (user_id, is_active)
habit_entries: habit_id, (habit_id, entry_date)
foods: user_id, (user_id, meal_date)
workouts: user_id, (user_id, workout_date)
daily_reviews: user_id, (user_id, review_date)
blog_entries: user_id, slug, (status, published_at)
tags: name, slug
taggables: tag_id, (taggable_type, taggable_id)
```

---

## Cascade Behavior

```
DELETE user → CASCADE all related data
DELETE goal → CASCADE goal_progress, SET NULL parent_goal_id
DELETE habit → CASCADE habit_entries
DELETE workout → CASCADE workout_exercises
DELETE tag → CASCADE taggables
```

---

## Unique Constraints

```
users: (email), (username)
blog_entries: (slug)
tags: (slug)
habit_entries: (habit_id, entry_date)
daily_reviews: (user_id, review_date)
taggables: (tag_id, taggable_type, taggable_id)
progress_snapshots: (user_id, snapshot_date, snapshot_type)
```

---

## Typical Workflows

### 1. Daily Check-In
```
1. Mark habits as completed → habit_entries
2. Log meals → foods
3. Log workout (if any) → workouts + workout_exercises
4. End-of-day review → daily_reviews
```

### 2. Goal Setting
```
1. Create goal → goals
2. Track progress → goal_progress
3. Update status when completed
4. View analytics via progress_snapshots
```

### 3. Habit Building
```
1. Create habit → habits
2. Daily completion → habit_entries
3. Update streak counts
4. View trends and statistics
```

### 4. Content Creation
```
1. Write blog entry → blog_entries (draft)
2. Add tags → taggables
3. Upload media → media
4. Publish → update status
```

---

## API Endpoint Patterns

### RESTful Routes

```
GET    /api/v1/goals              - List goals
POST   /api/v1/goals              - Create goal
GET    /api/v1/goals/{id}         - Get goal
PUT    /api/v1/goals/{id}         - Update goal
DELETE /api/v1/goals/{id}         - Delete goal
GET    /api/v1/goals/{id}/progress - Get progress
POST   /api/v1/goals/{id}/progress - Add progress

Similar patterns for:
- /habits
- /foods
- /workouts
- /daily-reviews
- /blog-entries
```

---

## Performance Tips

1. **Use SELECT specific columns** instead of `SELECT *`
2. **Eager load relationships** with `joinedload()` or `selectinload()`
3. **Paginate large result sets** with `LIMIT` and `OFFSET`
4. **Use database aggregations** instead of application-level calculations
5. **Create composite indexes** for multi-column filters
6. **Batch insert** with `bulk_save_objects()` for multiple records
7. **Use connection pooling** for production
8. **Monitor slow queries** with query logging

---

## Testing Queries

```bash
# Connect to database
psql -U lets_manifest_user -d lets_manifest_dev

# Check table
\d goals

# Sample queries
SELECT COUNT(*) FROM users;
SELECT * FROM goals WHERE user_id = '...' LIMIT 5;
EXPLAIN ANALYZE SELECT * FROM habits WHERE user_id = '...';
```

---

## Migration Commands

```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1

# Check current version
alembic current

# View history
alembic history
```

---

## Troubleshooting

### Common Issues

1. **Foreign Key Violation**
   - Ensure parent record exists before creating child
   - Check CASCADE settings

2. **Unique Constraint Violation**
   - Check for duplicate email/username/slug
   - Verify unique constraints on combined columns

3. **Check Constraint Violation**
   - Verify enum values match CHECK constraints
   - Validate rating ranges (1-10)

4. **N+1 Query Problem**
   - Use eager loading with `joinedload()`
   - Check SQLAlchemy query logs

5. **Slow Queries**
   - Add appropriate indexes
   - Use `EXPLAIN ANALYZE` to check query plan
   - Consider denormalization for read-heavy tables

---

## Quick SQL Snippets

```sql
-- Reset sequence (if needed)
ALTER SEQUENCE table_name_id_seq RESTART WITH 1;

-- Check table size
SELECT pg_size_pretty(pg_total_relation_size('table_name'));

-- Find unused indexes
SELECT * FROM pg_stat_user_indexes WHERE idx_scan = 0;

-- Active connections
SELECT count(*) FROM pg_stat_activity;

-- Kill connection
SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE ...;
```

---

For complete documentation, see:
- [DATABASE_SCHEMA.md](./DATABASE_SCHEMA.md) - Complete table definitions
- [ER_DIAGRAM.md](./ER_DIAGRAM.md) - Visual relationship diagrams
- [IMPLEMENTATION_GUIDE.md](./IMPLEMENTATION_GUIDE.md) - Detailed implementation examples
- [schema.sql](./schema.sql) - Raw SQL schema
