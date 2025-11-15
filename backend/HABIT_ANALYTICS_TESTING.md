# Habit Analytics Testing Guide

## Overview

This document describes the testing strategy for the habit streak tracking and analytics features.

## Test Files

### Backend Tests

#### `tests/unit/test_habit_analytics_service.py`

Comprehensive unit tests for the `HabitAnalyticsService` covering:

**Daily Streak Calculation Tests:**
- `test_zero_streak_no_entries` - Verifies zero streak with no entries
- `test_single_day_streak` - Tests single day streak calculation
- `test_consecutive_streak` - Tests consecutive daily streaks (5 days)
- `test_broken_streak` - Verifies streak breaks when a day is missed
- `test_inactive_streak_yesterday` - Tests streak is still active for yesterday
- `test_inactive_streak_two_days_ago` - Tests streak becomes inactive after 2+ days

**Weekly Streak Calculation Tests:**
- `test_weekly_streak_current_week` - Tests weekly streak for current week
- `test_weekly_consecutive_streak` - Tests consecutive weekly streaks (3 weeks)

**Completion Statistics Tests:**
- `test_completion_stats_no_entries` - Tests stats with no entries
- `test_completion_stats_with_entries` - Tests stats with mixed complete/incomplete entries
  - Validates total completions
  - Validates completion rate calculation
  - Validates current week/month aggregations

**Habit Analytics Tests:**
- `test_habit_analytics_with_good_performance` - Tests analytics for high-performing habits
- `test_confidence_level_calculation` - Verifies confidence level increases with better performance

**Streak Recovery Tests:**
- `test_can_recover_within_grace_period` - Tests recovery is allowed within grace period
- `test_cannot_recover_outside_grace_period` - Tests recovery is denied outside grace period

## Running Tests

### Prerequisites

1. PostgreSQL database running (for integration tests)
2. Test database configuration in settings
3. Required Python packages installed:
   ```bash
   pip install -r requirements-dev.txt
   ```

### Running All Tests

```bash
cd backend
pytest tests/unit/test_habit_analytics_service.py -v
```

### Running Specific Test Classes

```bash
# Daily streak tests
pytest tests/unit/test_habit_analytics_service.py::TestDailyStreakCalculation -v

# Weekly streak tests
pytest tests/unit/test_habit_analytics_service.py::TestWeeklyStreakCalculation -v

# Completion stats tests
pytest tests/unit/test_habit_analytics_service.py::TestCompletionStats -v

# Analytics tests
pytest tests/unit/test_habit_analytics_service.py::TestHabitAnalytics -v

# Recovery tests
pytest tests/unit/test_habit_analytics_service.py::TestStreakRecovery -v
```

### Running Individual Tests

```bash
pytest tests/unit/test_habit_analytics_service.py::TestDailyStreakCalculation::test_consecutive_streak -v
```

## Test Coverage

The test suite covers:

### Streak Calculation Logic ✅
- Daily habit streaks
- Weekly habit streaks
- Monthly habit streaks (via service implementation)
- Consecutive completion tracking
- Streak break detection
- Active vs inactive streak determination

### Completion Statistics ✅
- Total completions counting
- Completion rate calculation
- Current week/month aggregations
- Days tracked counting

### Analytics Integration ✅
- Confidence level calculation
- Motivational message generation
- Combined streak + stats analytics

### Streak Recovery ✅
- Grace period validation
- Recovery eligibility checking
- Deadline calculation

## Manual Testing Scenarios

### Scenario 1: Daily Habit Streak Building

**Test Steps:**
1. Create a daily habit
2. Mark it complete for today
3. Verify current streak = 1, active = true
4. Mark it complete for yesterday (recovery)
5. Verify current streak = 2
6. Continue for 7 days
7. Verify streak = 7, longest = 7

**Expected Results:**
- Streak increments correctly
- Active status maintained
- Longest streak tracked

### Scenario 2: Streak Break and Recovery

**Test Steps:**
1. Create a daily habit with 5-day streak
2. Skip a day (don't mark complete)
3. Verify streak becomes inactive
4. Use recovery endpoint within grace period
5. Verify streak is restored
6. Try recovery after grace period
7. Verify recovery is rejected

**Expected Results:**
- Streak breaks after grace period
- Recovery works within grace period
- Recovery rejected outside grace period

### Scenario 3: Weekly Habit Tracking

**Test Steps:**
1. Create a weekly habit (target 1 day/week)
2. Complete once this week
3. Verify streak = 1, active = true
4. Complete once next week
5. Verify streak = 2
6. Skip a week
7. Verify streak resets

**Expected Results:**
- Weekly streak tracks correctly
- Missing a week breaks streak
- Active status based on current week

### Scenario 4: Analytics Dashboard

**Test Steps:**
1. Navigate to habit analytics page
2. Verify all components display:
   - Streak information
   - Completion stats
   - Calendar view
   - Motivational insights
3. Change time period (30/90/180/365 days)
4. Verify data updates correctly
5. Check confidence level indicator
6. Verify trend direction

**Expected Results:**
- All visualizations render
- Data is accurate
- Time period selector works
- Responsive design works on mobile

### Scenario 5: User Insights Summary

**Test Steps:**
1. Create multiple habits with varying performance
2. View habits page
3. Verify insights summary shows:
   - Total active streaks
   - Average streak length
   - Overall completion rate
   - Motivational messages
4. Verify best performing habits listed
5. Verify habits needing attention listed

**Expected Results:**
- Aggregated stats are accurate
- Best/worst performers identified correctly
- Insights are motivating and relevant

## Frontend Component Testing

### Components to Test

1. **StreakDisplay**
   - Renders current/longest streaks
   - Shows appropriate emoji and description
   - Displays active badge correctly

2. **CompletionStats**
   - Shows all statistics
   - Confidence meter renders correctly
   - Color coding matches confidence level

3. **CompletionCalendar**
   - Displays months correctly
   - Shows completed/missed days
   - Hover tooltips work
   - Legend is accurate

4. **MotivationalInsights**
   - Displays main message
   - Shows multiple insights
   - Gradient background renders

5. **HabitAnalyticsDashboard**
   - Integrates all sub-components
   - Time period selector works
   - Loading states display
   - Error handling works

## API Endpoint Testing

### Endpoints to Test

```bash
# Get habit analytics
GET /api/v1/habits/{habit_id}/analytics

# Get progress trends
GET /api/v1/habits/{habit_id}/progress?days=90

# Check streak recovery
GET /api/v1/habits/{habit_id}/streak-recovery?grace_days=1

# Get user insights
GET /api/v1/habits/insights

# Reset streak
POST /api/v1/habits/{habit_id}/reset-streak

# Recover streak
POST /api/v1/habits/{habit_id}/recover-streak?recovery_date=2025-01-15
```

### Using curl Examples

```bash
# Get analytics
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/v1/habits/{habit_id}/analytics

# Recover streak
curl -X POST -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/v1/habits/{habit_id}/recover-streak?recovery_date=2025-01-15"
```

## Test Data Setup

### Creating Test Habits

```python
# Daily habit with 7-day streak
habit = create_habit(name="Exercise", frequency="daily")
for i in range(7):
    create_entry(habit_id, date.today() - timedelta(days=i), completed=True)

# Weekly habit with 4-week streak
habit = create_habit(name="Review", frequency="weekly")
for i in range(4):
    create_entry(habit_id, date.today() - timedelta(weeks=i), completed=True)

# Habit with broken streak
habit = create_habit(name="Reading", frequency="daily")
for i in [0, 1, 2, 4, 5]:  # Missing day 3
    create_entry(habit_id, date.today() - timedelta(days=i), completed=True)
```

## Continuous Integration

Tests should be run in CI/CD pipeline:

```yaml
# Example GitHub Actions workflow
- name: Run Backend Tests
  run: |
    cd backend
    pytest tests/unit/test_habit_analytics_service.py -v --cov=app
```

## Performance Considerations

### Test Execution Time
- Unit tests should complete in < 5 seconds per test
- Integration tests may take longer due to database operations

### Database Optimization
- Use test database separate from development
- Clean up test data after each test
- Use fixtures for common test data

## Future Test Enhancements

1. **Integration Tests**
   - End-to-end API testing
   - Full workflow testing
   - Database persistence verification

2. **Performance Tests**
   - Large dataset handling
   - Concurrent user scenarios
   - Query optimization validation

3. **Frontend E2E Tests**
   - User interaction flows
   - Cross-browser testing
   - Mobile responsiveness

4. **Load Testing**
   - Analytics endpoint performance
   - Concurrent streak calculations
   - Database query optimization

## Known Issues and Limitations

1. Tests require PostgreSQL database
2. Async test execution needs proper event loop setup
3. Time-dependent tests may be flaky
4. Some edge cases around month/year boundaries

## Debugging Tips

1. **Failing Streak Tests**
   - Check date calculations
   - Verify timezone handling
   - Inspect database entry dates

2. **Analytics Test Failures**
   - Validate data setup
   - Check floating point comparisons
   - Verify aggregation logic

3. **Recovery Test Issues**
   - Confirm grace period logic
   - Check date comparisons
   - Validate error messages
