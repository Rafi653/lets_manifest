# Entity Relationship Diagram

## Let's Manifest Database Schema - Visual Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              USERS (Central Entity)                              │
│  ┌───────────────────────────────────────────────────────────────────────────┐  │
│  │ • Authentication & Profile                                                │  │
│  │ • User preferences and settings                                           │  │
│  └───────────────────────────────────────────────────────────────────────────┘  │
└────────┬─────────────┬─────────────┬─────────────┬─────────────┬────────────────┘
         │             │             │             │             │
    ┌────▼───┐    ┌───▼────┐   ┌───▼────┐   ┌───▼────┐   ┌───▼────┐
    │ GOALS  │    │ HABITS │   │ FOODS  │   │WORKOUTS│   │ REVIEWS│
    └────┬───┘    └───┬────┘   └────────┘   └───┬────┘   └────────┘
         │            │                          │
    ┌────▼───────┐ ┌─▼───────────┐       ┌──────▼──────────┐
    │  PROGRESS  │ │HABIT_ENTRIES│       │WORKOUT_EXERCISES│
    └────────────┘ └─────────────┘       └─────────────────┘
```

### Detailed Entity Relationships

#### 1. User-Centric Modules

```
                                    users
                                      │
                    ┌─────────────────┼─────────────────┐
                    │                 │                 │
                  goals            habits          daily_reviews
                    │                 │
              goal_progress    habit_entries
```

**Relationships:**
- 1 user → many goals
- 1 user → many habits
- 1 user → many daily_reviews
- 1 goal → many goal_progress entries
- 1 habit → many habit_entries

#### 2. Health & Fitness Modules

```
                    users
                      │
        ┌─────────────┼─────────────┐
        │             │             │
      foods       workouts     progress_snapshots
                      │
              workout_exercises
```

**Relationships:**
- 1 user → many foods
- 1 user → many workouts
- 1 user → many progress_snapshots
- 1 workout → many workout_exercises

#### 3. Content & Media Modules

```
                    users
                      │
        ┌─────────────┼─────────────┐
        │             │             │
   blog_entries     media         tags
        │                           │
        └──────────┬────────────────┘
                   │
               taggables (polymorphic)
```

**Relationships:**
- 1 user → many blog_entries
- 1 user → many media files
- Many entities ↔ many tags (via taggables)

### Complete ER Diagram

```
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│                              USERS TABLE                                   │
│  ┌──────────────────────────────────────────────────────────────────┐    │
│  │ PK: id (UUID)                                                     │    │
│  │ • email (unique)                                                  │    │
│  │ • username (unique)                                               │    │
│  │ • password_hash                                                   │    │
│  │ • profile fields (name, avatar, bio)                             │    │
│  │ • settings (timezone, is_active, is_verified)                    │    │
│  │ • timestamps (created_at, updated_at, last_login_at)            │    │
│  └──────────────────────────────────────────────────────────────────┘    │
│                                                                            │
└──────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┬──────┘
       │         │         │         │         │         │         │
       │         │         │         │         │         │         │
┌──────▼─────┐ ┌─▼──────┐ ┌▼──────┐ ┌▼──────┐ ┌▼──────┐ ┌▼──────┐ ┌▼──────┐
│   GOALS    │ │ HABITS │ │ FOODS │ │WORKOUTS││ REVIEWS││  BLOG  ││ MEDIA │
├────────────┤ ├────────┤ ├───────┤ ├────────┤ ├────────┤ ├───────┤ ├───────┤
│PK: id      │ │PK: id  │ │PK: id │ │PK: id  │ │PK: id  │ │PK: id │ │PK: id │
│FK: user_id │ │FK:     │ │FK:    │ │FK:     │ │FK:     │ │FK:    │ │FK:    │
│            │ │user_id │ │user_id│ │user_id │ │user_id │ │user_id│ │user_id│
│• title     │ │• name  │ │• meal │ │• workout│ │• review│ │• title│ │• file │
│• type      │ │• freq  │ │  _type│ │  _type │ │  _date │ │• slug │ │  info │
│• dates     │ │• streak│ │• nutri│ │• duration│ │• mood │ │• status│ │• size│
│• status    │ │• active│ │  tion │ │• calories│ │• energy│ │• public│ │• type│
│• priority  │ │        │ │       │ │         │ │• sleep │ │       │ │      │
└──────┬─────┘ └────┬───┘ └───────┘ └────┬───┘ └────────┘ └───────┘ └──────┘
       │            │                     │
┌──────▼─────┐ ┌────▼────┐         ┌─────▼─────┐
│   GOAL     │ │  HABIT  │         │  WORKOUT  │
│  PROGRESS  │ │ ENTRIES │         │ EXERCISES │
├────────────┤ ├─────────┤         ├───────────┤
│PK: id      │ │PK: id   │         │PK: id     │
│FK: goal_id │ │FK:      │         │FK:        │
│            │ │habit_id │         │workout_id │
│• date      │ │• date   │         │• exercise │
│• value     │ │• complete│        │• sets/reps│
│• notes     │ │• mood   │         │• weight   │
└────────────┘ └─────────┘         └───────────┘


┌─────────────────────────────────────────────────────────────────┐
│                    SUPPORTING TABLES                            │
├─────────────────┬──────────────────┬──────────────────────────┤
│     TAGS        │    TAGGABLES     │   PROGRESS_SNAPSHOTS     │
├─────────────────┼──────────────────┼──────────────────────────┤
│ PK: id          │ PK: id           │ PK: id                   │
│ • name          │ FK: tag_id       │ FK: user_id              │
│ • slug          │ • taggable_id    │ • snapshot_date          │
│ • category      │ • taggable_type  │ • snapshot_type          │
│ • color         │   (polymorphic)  │ • aggregated_metrics     │
│ • usage_count   │                  │ • health_data            │
└─────────────────┴──────────────────┴──────────────────────────┘
```

### Table Relationship Types

#### One-to-Many Relationships
```
users (1) ──→ (∞) goals
users (1) ──→ (∞) habits
users (1) ──→ (∞) foods
users (1) ──→ (∞) workouts
users (1) ──→ (∞) daily_reviews
users (1) ──→ (∞) blog_entries
users (1) ──→ (∞) media
users (1) ──→ (∞) progress_snapshots

goals (1) ──→ (∞) goal_progress
habits (1) ──→ (∞) habit_entries
workouts (1) ──→ (∞) workout_exercises
```

#### Self-Referential Relationships
```
goals (parent) ──→ (children) goals
    via parent_goal_id
```

#### Many-to-Many via Polymorphic Table
```
tags (∞) ←→ (∞) goals
tags (∞) ←→ (∞) habits
tags (∞) ←→ (∞) blog_entries
tags (∞) ←→ (∞) workouts
tags (∞) ←→ (∞) foods
    via taggables (polymorphic junction table)
```

### Polymorphic Relationships

#### Taggables (Polymorphic Association)
```
┌──────────┐
│   tags   │
└────┬─────┘
     │
┌────▼────────┐
│  taggables  │  ← Junction table
├─────────────┤
│ tag_id      │
│ taggable_id │  ← Points to any entity
│ taggable_   │
│ type        │  ← Specifies which table
└─────┬───────┘
      │
      ├──→ goals
      ├──→ habits
      ├──→ blog_entries
      ├──→ workouts
      └──→ foods
```

#### Media (Polymorphic Association)
```
┌───────────┐
│   media   │
├───────────┤
│ id        │
│ user_id   │
│ file_*    │
│ related_  │
│ to_type   │  ← Entity type
│ related_  │
│ to_id     │  ← Entity ID
└─────┬─────┘
      │
      ├──→ goals
      ├──→ blog_entries
      ├──→ workouts
      ├──→ users (avatar)
      └──→ any other entity
```

### Cardinality Summary

| Relationship | Type | Description |
|-------------|------|-------------|
| users → goals | 1:M | One user has many goals |
| users → habits | 1:M | One user has many habits |
| users → foods | 1:M | One user has many food entries |
| users → workouts | 1:M | One user has many workouts |
| users → daily_reviews | 1:M | One user has many daily reviews |
| users → blog_entries | 1:M | One user has many blog entries |
| users → media | 1:M | One user has many media files |
| users → progress_snapshots | 1:M | One user has many snapshots |
| goals → goal_progress | 1:M | One goal has many progress entries |
| habits → habit_entries | 1:M | One habit has many entries |
| workouts → workout_exercises | 1:M | One workout has many exercises |
| goals → goals | 1:M (self) | Goals can have sub-goals |
| tags ↔ * | M:M | Tags can be applied to many entities |

### Data Flow Patterns

#### 1. Goal Tracking Flow
```
User creates Goal
     ↓
Goal is saved with target metrics
     ↓
User updates progress regularly
     ↓
Progress entries are recorded
     ↓
Goal status updated (active → completed)
     ↓
Aggregated in progress_snapshots
```

#### 2. Habit Streak Flow
```
User creates Habit with frequency
     ↓
Daily habit_entry created/updated
     ↓
Streak calculation (current_streak)
     ↓
Longest streak tracking
     ↓
Aggregated in progress_snapshots
```

#### 3. Food Tracking Flow
```
User logs food entry
     ↓
Nutrition data calculated
     ↓
Daily summary aggregated
     ↓
Weekly/monthly trends
     ↓
Included in progress_snapshots
```

#### 4. Workout Flow
```
User starts workout
     ↓
Workout created with metadata
     ↓
Exercises added to workout
     ↓
Performance metrics recorded
     ↓
Statistics aggregated
     ↓
Included in progress_snapshots
```

#### 5. Daily Review Flow
```
End of day
     ↓
User creates daily_review
     ↓
Mood, energy, productivity rated
     ↓
Reflections recorded
     ↓
Trends analyzed over time
     ↓
Aggregated in progress_snapshots
```

### Index Strategy Visualization

```
┌─────────────────────────────────────────────┐
│            PRIMARY INDEXES                   │
├─────────────────────────────────────────────┤
│ • All tables: id (UUID, Primary Key)        │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│          FOREIGN KEY INDEXES                 │
├─────────────────────────────────────────────┤
│ • user_id (on all user-owned tables)        │
│ • goal_id, habit_id, workout_id, etc.       │
│ • parent_goal_id, tag_id, etc.              │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│          COMPOSITE INDEXES                   │
├─────────────────────────────────────────────┤
│ • (user_id, status) - goals                 │
│ • (user_id, entry_date) - habit_entries     │
│ • (user_id, meal_date) - foods              │
│ • (user_id, workout_date) - workouts        │
│ • (taggable_type, taggable_id) - taggables  │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│            UNIQUE INDEXES                    │
├─────────────────────────────────────────────┤
│ • email, username - users                   │
│ • slug - blog_entries, tags                 │
│ • (habit_id, entry_date) - habit_entries    │
│ • (user_id, review_date) - daily_reviews    │
└─────────────────────────────────────────────┘
```

### Cascade Behavior

```
DELETE user
    ├→ CASCADE delete all goals
    │      └→ CASCADE delete all goal_progress
    ├→ CASCADE delete all habits
    │      └→ CASCADE delete all habit_entries
    ├→ CASCADE delete all foods
    ├→ CASCADE delete all workouts
    │      └→ CASCADE delete all workout_exercises
    ├→ CASCADE delete all daily_reviews
    ├→ CASCADE delete all blog_entries
    ├→ CASCADE delete all media
    └→ CASCADE delete all progress_snapshots

DELETE goal
    ├→ CASCADE delete all goal_progress
    └→ SET NULL for child goals (parent_goal_id)

DELETE habit
    └→ CASCADE delete all habit_entries

DELETE workout
    └→ CASCADE delete all workout_exercises

DELETE tag
    └→ CASCADE delete all taggables
```

### Query Access Patterns

```
Most Common Queries:

1. Get user's active goals
   SELECT * FROM goals WHERE user_id = ? AND status = 'active'
   Uses: idx_goals_user_status

2. Get habit streak data
   SELECT * FROM habit_entries WHERE habit_id = ? ORDER BY entry_date
   Uses: idx_habit_entries_date

3. Get daily food summary
   SELECT * FROM foods WHERE user_id = ? AND meal_date = ?
   Uses: idx_foods_user_date

4. Get workout history
   SELECT * FROM workouts WHERE user_id = ? ORDER BY workout_date DESC
   Uses: idx_workouts_user_date

5. Get tagged entities
   SELECT * FROM taggables WHERE taggable_type = ? AND tag_id = ?
   Uses: idx_taggables_polymorphic

6. Get user's progress over time
   SELECT * FROM progress_snapshots WHERE user_id = ? ORDER BY snapshot_date
   Uses: idx_progress_snapshots_date
```

### Constraint Summary

```
CHECK Constraints:
├─ goal_type IN ('daily', 'weekly', 'monthly', 'yearly')
├─ status IN ('active', 'completed', 'cancelled', 'paused')
├─ priority BETWEEN 0 AND 5
├─ mood_rating BETWEEN 1 AND 10
├─ energy_level BETWEEN 1 AND 10
├─ meal_type IN ('breakfast', 'lunch', 'dinner', 'snack')
├─ intensity IN ('low', 'medium', 'high')
└─ weight_unit IN ('lbs', 'kg')

UNIQUE Constraints:
├─ users (email), (username)
├─ blog_entries (slug)
├─ tags (slug)
├─ habit_entries (habit_id, entry_date)
├─ daily_reviews (user_id, review_date)
├─ taggables (tag_id, taggable_type, taggable_id)
└─ progress_snapshots (user_id, snapshot_date, snapshot_type)

NOT NULL Constraints:
├─ All user_id foreign keys
├─ All title/name fields
├─ All date fields for time-based entries
└─ Essential fields for data integrity
```

## Implementation Notes

1. **UUID Primary Keys**: All tables use UUID for better distribution and security
2. **Timestamps**: created_at/updated_at on all major tables with automatic triggers
3. **Soft Deletes**: Not implemented; using hard deletes with CASCADE
4. **Indexing**: Comprehensive indexing for common query patterns
5. **Constraints**: Strong data integrity through CHECK and UNIQUE constraints
6. **Polymorphic**: taggables and media support flexible associations
7. **Triggers**: Auto-update triggers for updated_at columns

## Future Considerations

1. Add partitioning for time-series data (foods, workouts, habit_entries)
2. Consider materialized views for complex analytics queries
3. Add full-text search indexes for blog_entries content
4. Implement audit logging tables for sensitive operations
5. Add notification preferences and history tables
6. Consider read replicas for scaling read-heavy workloads
