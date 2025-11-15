# Database Schema Implementation Guide

## Overview

This guide provides a comprehensive overview of the database schema implementation for the Let's Manifest application, including practical examples and best practices.

## Table of Contents

1. [Schema Organization](#schema-organization)
2. [Key Design Decisions](#key-design-decisions)
3. [Implementation Examples](#implementation-examples)
4. [Common Query Patterns](#common-query-patterns)
5. [Migration Strategy](#migration-strategy)
6. [Testing Recommendations](#testing-recommendations)

---

## Schema Organization

### Module Structure

The database is organized into logical modules:

#### 1. **Core Module**
- `users` - Authentication and user profiles

#### 2. **Goal Tracking Module**
- `goals` - Goal definitions and tracking
- `goal_progress` - Progress updates for goals

#### 3. **Habit Tracking Module**
- `habits` - Habit definitions
- `habit_entries` - Daily habit completion records

#### 4. **Health & Fitness Module**
- `foods` - Food and nutrition tracking
- `workouts` - Workout sessions
- `workout_exercises` - Individual exercises in workouts

#### 5. **Reflection Module**
- `daily_reviews` - End-of-day reflections
- `blog_entries` - Blog posts and journal entries

#### 6. **Supporting Modules**
- `tags` - Tagging system
- `taggables` - Polymorphic tag associations
- `media` - File uploads
- `progress_snapshots` - Aggregated progress tracking

---

## Key Design Decisions

### 1. UUID Primary Keys

**Decision:** Use UUID instead of auto-incrementing integers.

**Rationale:**
- Better for distributed systems
- Prevents enumeration attacks
- No collision concerns when merging data
- Enables client-side ID generation

**Example:**
```python
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID

id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
```

### 2. Polymorphic Associations

**Decision:** Use polymorphic tables for tags and media.

**Rationale:**
- Flexible association with any entity type
- Single tagging system for all modules
- Reduces table proliferation

**Example:**
```python
# Tag a goal
taggable = Taggable(
    tag_id=tag.id,
    taggable_id=goal.id,
    taggable_type='goal'
)
```

### 3. Soft vs Hard Deletes

**Decision:** Use hard deletes with CASCADE.

**Rationale:**
- Simpler implementation
- No "deleted" records cluttering database
- GDPR compliance easier (right to be forgotten)
- Can implement soft deletes later if needed

### 4. Timestamps on All Tables

**Decision:** Include created_at and updated_at on all tables.

**Rationale:**
- Audit trail
- Debugging and troubleshooting
- Analytics and reporting
- User-facing features (e.g., "Last updated")

### 5. Check Constraints for Enums

**Decision:** Use CHECK constraints instead of separate enum tables.

**Rationale:**
- Simpler schema
- Better performance
- Easier to maintain
- PostgreSQL validates at database level

**Example:**
```sql
CHECK (status IN ('active', 'completed', 'cancelled', 'paused'))
```

---

## Implementation Examples

### Creating a Goal with Progress Tracking

```python
from datetime import date, datetime
from decimal import Decimal
from sqlalchemy.orm import Session

from app.models import Goal, GoalProgress

# Create a goal
goal = Goal(
    user_id=user.id,
    title="Exercise 5 times per week",
    description="Complete at least 30 minutes of exercise 5 days per week",
    goal_type="weekly",
    category="health",
    target_value=Decimal("5"),
    target_unit="workouts",
    current_value=Decimal("0"),
    start_date=date.today(),
    end_date=date.today() + timedelta(days=7),
    status="active",
    priority=3
)

db.add(goal)
db.commit()

# Add progress entry
progress = GoalProgress(
    goal_id=goal.id,
    progress_date=date.today(),
    value=Decimal("2"),
    percentage=Decimal("40.00"),
    notes="Completed 2 workouts so far"
)

db.add(progress)
db.commit()
```

### Tracking Habit Streaks

```python
from datetime import date, datetime
from sqlalchemy.orm import Session

from app.models import Habit, HabitEntry

# Create a habit
habit = Habit(
    user_id=user.id,
    name="Meditate",
    description="10 minutes of meditation each morning",
    frequency="daily",
    category="mindfulness",
    color="#4CAF50",
    is_active=True,
    current_streak=0,
    longest_streak=0,
    total_completions=0
)

db.add(habit)
db.commit()

# Mark habit as completed for today
entry = HabitEntry(
    habit_id=habit.id,
    entry_date=date.today(),
    completed=True,
    completed_at=datetime.utcnow(),
    mood="calm"
)

db.add(entry)

# Update streak
habit.current_streak += 1
habit.total_completions += 1
if habit.current_streak > habit.longest_streak:
    habit.longest_streak = habit.current_streak

db.commit()
```

### Logging Food and Nutrition

```python
from datetime import date, time
from decimal import Decimal
from sqlalchemy.orm import Session

from app.models import Food

# Log breakfast
food = Food(
    user_id=user.id,
    meal_date=date.today(),
    meal_time=time(8, 30),
    meal_type="breakfast",
    food_name="Oatmeal with berries",
    portion_size="1 cup",
    calories=Decimal("350"),
    protein_grams=Decimal("12"),
    carbs_grams=Decimal("58"),
    fats_grams=Decimal("8"),
    fiber_grams=Decimal("10"),
    is_favorite=True
)

db.add(food)
db.commit()
```

### Creating a Workout with Exercises

```python
from datetime import date, time
from decimal import Decimal
from sqlalchemy.orm import Session

from app.models import Workout, WorkoutExercise

# Create workout
workout = Workout(
    user_id=user.id,
    workout_date=date.today(),
    workout_time=time(18, 0),
    workout_type="strength",
    workout_name="Upper Body Day",
    duration_minutes=60,
    calories_burned=Decimal("350"),
    intensity="high",
    location="Gym",
    mood_before="tired",
    mood_after="energized"
)

db.add(workout)
db.flush()  # Get workout.id

# Add exercises
exercises = [
    WorkoutExercise(
        workout_id=workout.id,
        exercise_name="Bench Press",
        exercise_type="barbell",
        sets=4,
        reps=10,
        weight=Decimal("185"),
        weight_unit="lbs",
        order_index=0
    ),
    WorkoutExercise(
        workout_id=workout.id,
        exercise_name="Pull-ups",
        exercise_type="bodyweight",
        sets=3,
        reps=12,
        order_index=1
    ),
    WorkoutExercise(
        workout_id=workout.id,
        exercise_name="Shoulder Press",
        exercise_type="dumbbell",
        sets=3,
        reps=12,
        weight=Decimal("50"),
        weight_unit="lbs",
        order_index=2
    )
]

db.add_all(exercises)
db.commit()
```

### Daily Review

```python
from datetime import date
from sqlalchemy.orm import Session

from app.models import DailyReview

# Create daily review
review = DailyReview(
    user_id=user.id,
    review_date=date.today(),
    mood_rating=8,
    energy_level=7,
    productivity_rating=9,
    sleep_hours=Decimal("7.5"),
    sleep_quality=8,
    water_intake_ml=2500,
    accomplishments="Completed all workout goals. Finished project milestone.",
    challenges="Had trouble focusing in the afternoon",
    lessons_learned="Morning workouts boost my energy for the day",
    gratitude="Grateful for supportive team and good health",
    tomorrow_intentions="Start work 30 minutes earlier",
    highlights="Great team meeting and productive workout"
)

db.add(review)
db.commit()
```

### Tagging Entities

```python
from sqlalchemy.orm import Session

from app.models import Tag, Taggable

# Create tags
tag_fitness = Tag(
    name="Fitness",
    slug="fitness",
    category="health",
    color="#FF5722"
)

tag_strength = Tag(
    name="Strength Training",
    slug="strength-training",
    category="health",
    color="#E91E63"
)

db.add_all([tag_fitness, tag_strength])
db.commit()

# Tag a workout
taggables = [
    Taggable(
        tag_id=tag_fitness.id,
        taggable_id=workout.id,
        taggable_type="workout"
    ),
    Taggable(
        tag_id=tag_strength.id,
        taggable_id=workout.id,
        taggable_type="workout"
    )
]

db.add_all(taggables)

# Update usage counts
tag_fitness.usage_count += 1
tag_strength.usage_count += 1

db.commit()
```

---

## Common Query Patterns

### 1. Get User's Active Goals

```python
from sqlalchemy import and_
from app.models import Goal

# Get active goals ordered by priority and end date
active_goals = (
    db.query(Goal)
    .filter(
        and_(
            Goal.user_id == user_id,
            Goal.status == "active"
        )
    )
    .order_by(Goal.priority.desc(), Goal.end_date.asc())
    .all()
)
```

### 2. Calculate Habit Completion Rate

```python
from datetime import date, timedelta
from sqlalchemy import and_, func
from app.models import Habit, HabitEntry

# Get habit completion rate for last 30 days
start_date = date.today() - timedelta(days=30)

habit_stats = (
    db.query(
        Habit.id,
        Habit.name,
        func.count(HabitEntry.id).label("total_entries"),
        func.sum(func.cast(HabitEntry.completed, Integer)).label("completed_count")
    )
    .join(HabitEntry)
    .filter(
        and_(
            Habit.user_id == user_id,
            HabitEntry.entry_date >= start_date
        )
    )
    .group_by(Habit.id, Habit.name)
    .all()
)

# Calculate completion rate
for habit in habit_stats:
    completion_rate = (habit.completed_count / habit.total_entries * 100) if habit.total_entries > 0 else 0
    print(f"{habit.name}: {completion_rate:.1f}%")
```

### 3. Get Daily Nutrition Summary

```python
from datetime import date
from sqlalchemy import and_, func
from app.models import Food

# Get nutrition summary for today
summary = (
    db.query(
        func.sum(Food.calories).label("total_calories"),
        func.sum(Food.protein_grams).label("total_protein"),
        func.sum(Food.carbs_grams).label("total_carbs"),
        func.sum(Food.fats_grams).label("total_fats")
    )
    .filter(
        and_(
            Food.user_id == user_id,
            Food.meal_date == date.today()
        )
    )
    .first()
)

print(f"Calories: {summary.total_calories}")
print(f"Protein: {summary.total_protein}g")
print(f"Carbs: {summary.total_carbs}g")
print(f"Fats: {summary.total_fats}g")
```

### 4. Get Workout History with Exercises

```python
from sqlalchemy.orm import joinedload
from app.models import Workout

# Get last 10 workouts with exercises
workouts = (
    db.query(Workout)
    .options(joinedload(Workout.exercises))
    .filter(Workout.user_id == user_id)
    .order_by(Workout.workout_date.desc())
    .limit(10)
    .all()
)

for workout in workouts:
    print(f"{workout.workout_date}: {workout.workout_name}")
    for exercise in workout.exercises:
        print(f"  - {exercise.exercise_name}: {exercise.sets}x{exercise.reps}")
```

### 5. Get Tagged Entities

```python
from sqlalchemy.orm import joinedload
from app.models import Tag, Taggable

# Get all goals with a specific tag
tag = db.query(Tag).filter(Tag.slug == "fitness").first()

tagged_goals = (
    db.query(Goal)
    .join(Taggable, and_(
        Taggable.taggable_id == Goal.id,
        Taggable.taggable_type == "goal"
    ))
    .filter(Taggable.tag_id == tag.id)
    .all()
)
```

### 6. Get Weekly Progress Trends

```python
from datetime import date, timedelta
from sqlalchemy import and_, func
from app.models import DailyReview

# Get weekly mood and energy trends
start_date = date.today() - timedelta(days=30)

trends = (
    db.query(
        func.date_trunc('week', DailyReview.review_date).label('week'),
        func.avg(DailyReview.mood_rating).label('avg_mood'),
        func.avg(DailyReview.energy_level).label('avg_energy'),
        func.avg(DailyReview.productivity_rating).label('avg_productivity')
    )
    .filter(
        and_(
            DailyReview.user_id == user_id,
            DailyReview.review_date >= start_date
        )
    )
    .group_by(func.date_trunc('week', DailyReview.review_date))
    .order_by(func.date_trunc('week', DailyReview.review_date))
    .all()
)

for trend in trends:
    print(f"Week {trend.week}: Mood={trend.avg_mood:.1f}, Energy={trend.avg_energy:.1f}")
```

---

## Migration Strategy

### Phase 1: Core Tables (Week 1)
1. Create `users` table
2. Create `tags` and `taggables` tables
3. Create `media` table
4. Test authentication and basic user operations

### Phase 2: Goals Module (Week 2)
1. Create `goals` table
2. Create `goal_progress` table
3. Implement CRUD operations
4. Test goal tracking workflows

### Phase 3: Habits Module (Week 3)
1. Create `habits` table
2. Create `habit_entries` table
3. Implement streak calculations
4. Test habit tracking and streaks

### Phase 4: Health & Fitness (Week 4)
1. Create `foods` table
2. Create `workouts` and `workout_exercises` tables
3. Implement nutrition calculations
4. Test workout logging

### Phase 5: Reviews & Content (Week 5)
1. Create `daily_reviews` table
2. Create `blog_entries` table
3. Implement reflection features
4. Test content creation

### Phase 6: Analytics (Week 6)
1. Create `progress_snapshots` table
2. Implement aggregation logic
3. Create analytics queries
4. Test reporting features

---

## Testing Recommendations

### Unit Tests

```python
import pytest
from datetime import date
from decimal import Decimal
from app.models import Goal, GoalProgress

def test_create_goal(db_session, test_user):
    """Test goal creation."""
    goal = Goal(
        user_id=test_user.id,
        title="Test Goal",
        goal_type="daily",
        start_date=date.today(),
        end_date=date.today(),
        status="active"
    )
    db_session.add(goal)
    db_session.commit()
    
    assert goal.id is not None
    assert goal.title == "Test Goal"
    assert goal.current_value == Decimal("0")

def test_goal_progress(db_session, test_goal):
    """Test adding goal progress."""
    progress = GoalProgress(
        goal_id=test_goal.id,
        progress_date=date.today(),
        value=Decimal("50"),
        percentage=Decimal("50.00")
    )
    db_session.add(progress)
    db_session.commit()
    
    assert len(test_goal.progress_entries) == 1
    assert test_goal.progress_entries[0].value == Decimal("50")
```

### Integration Tests

```python
import pytest
from datetime import date
from app.models import Habit, HabitEntry

def test_habit_streak_calculation(db_session, test_user):
    """Test habit streak calculation."""
    habit = Habit(
        user_id=test_user.id,
        name="Test Habit",
        frequency="daily",
        is_active=True
    )
    db_session.add(habit)
    db_session.commit()
    
    # Add 3 consecutive days
    for i in range(3):
        entry = HabitEntry(
            habit_id=habit.id,
            entry_date=date.today() - timedelta(days=i),
            completed=True
        )
        db_session.add(entry)
        habit.current_streak += 1
    
    db_session.commit()
    
    assert habit.current_streak == 3
    assert habit.total_completions == 3
```

### Performance Tests

```python
import pytest
from datetime import date, timedelta
from app.models import Food

def test_bulk_food_insert(db_session, test_user):
    """Test bulk food entry insertion."""
    foods = [
        Food(
            user_id=test_user.id,
            meal_date=date.today() - timedelta(days=i),
            meal_type="lunch",
            food_name=f"Test Food {i}",
            calories=500
        )
        for i in range(100)
    ]
    
    db_session.bulk_save_objects(foods)
    db_session.commit()
    
    count = db_session.query(Food).filter(Food.user_id == test_user.id).count()
    assert count == 100
```

---

## Best Practices

### 1. Use Transactions

```python
from sqlalchemy.orm import Session

def create_workout_with_exercises(db: Session, workout_data, exercises_data):
    """Create workout and exercises in a transaction."""
    try:
        workout = Workout(**workout_data)
        db.add(workout)
        db.flush()  # Get workout.id
        
        exercises = [WorkoutExercise(workout_id=workout.id, **ex) for ex in exercises_data]
        db.add_all(exercises)
        
        db.commit()
        return workout
    except Exception as e:
        db.rollback()
        raise e
```

### 2. Use Eager Loading

```python
from sqlalchemy.orm import joinedload

# Good: Load related data in one query
workouts = (
    db.query(Workout)
    .options(joinedload(Workout.exercises))
    .filter(Workout.user_id == user_id)
    .all()
)

# Bad: N+1 query problem
workouts = db.query(Workout).filter(Workout.user_id == user_id).all()
for workout in workouts:
    exercises = workout.exercises  # Triggers separate query
```

### 3. Use Indexes Effectively

```python
# Query uses index on (user_id, status)
goals = db.query(Goal).filter(
    Goal.user_id == user_id,
    Goal.status == "active"
).all()

# Query uses index on (user_id, meal_date)
foods = db.query(Food).filter(
    Food.user_id == user_id,
    Food.meal_date == date.today()
).all()
```

### 4. Validate Data

```python
from decimal import Decimal
from pydantic import BaseModel, validator

class GoalCreate(BaseModel):
    title: str
    goal_type: str
    target_value: Decimal
    
    @validator('goal_type')
    def validate_goal_type(cls, v):
        if v not in ['daily', 'weekly', 'monthly', 'yearly']:
            raise ValueError('Invalid goal type')
        return v
    
    @validator('target_value')
    def validate_target_value(cls, v):
        if v <= 0:
            raise ValueError('Target value must be positive')
        return v
```

---

## Conclusion

This database schema provides a comprehensive foundation for the Let's Manifest application. It supports:

- ✅ Goal tracking with progress monitoring
- ✅ Habit formation with streak tracking
- ✅ Food and nutrition logging
- ✅ Workout tracking with detailed exercise logs
- ✅ Daily reviews and reflections
- ✅ Blog entries and content creation
- ✅ Flexible tagging system
- ✅ Media management
- ✅ Long-term progress snapshots

The schema is designed for:
- **Performance**: Optimized indexes and query patterns
- **Scalability**: UUID keys and proper normalization
- **Flexibility**: Polymorphic associations for tags and media
- **Data Integrity**: Foreign keys, check constraints, and unique constraints
- **Maintainability**: Clear structure and comprehensive documentation

Next steps:
1. Create Alembic migrations
2. Implement Pydantic schemas
3. Build API endpoints
4. Add frontend integration
5. Deploy and monitor

For questions or suggestions, please refer to the main documentation or create an issue on GitHub.
