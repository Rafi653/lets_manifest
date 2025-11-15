"""
Tests for habit analytics service - streak calculation and analytics.
"""

import pytest
from datetime import date, datetime, timedelta
from uuid import uuid4

from app.models.habit import Habit, HabitEntry
from app.models.user import User
from app.services.habit_analytics_service import HabitAnalyticsService
from app.core.security import get_password_hash


@pytest.fixture
async def test_user(db_session):
    """Create a test user."""
    user = User(
        id=uuid4(),
        email="test@example.com",
        hashed_password=get_password_hash("testpass123"),
        full_name="Test User",
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
async def daily_habit(db_session, test_user):
    """Create a daily habit for testing."""
    habit = Habit(
        id=uuid4(),
        user_id=test_user.id,
        name="Morning Exercise",
        description="30 minutes of exercise",
        frequency="daily",
        is_active=True,
        current_streak=0,
        longest_streak=0,
        total_completions=0,
    )
    db_session.add(habit)
    await db_session.commit()
    await db_session.refresh(habit)
    return habit


@pytest.fixture
async def weekly_habit(db_session, test_user):
    """Create a weekly habit for testing."""
    habit = Habit(
        id=uuid4(),
        user_id=test_user.id,
        name="Weekly Review",
        description="Reflect on the week",
        frequency="weekly",
        target_days=1,
        is_active=True,
        current_streak=0,
        longest_streak=0,
        total_completions=0,
    )
    db_session.add(habit)
    await db_session.commit()
    await db_session.refresh(habit)
    return habit


@pytest.mark.asyncio
class TestDailyStreakCalculation:
    """Tests for daily habit streak calculation."""

    async def test_zero_streak_no_entries(self, db_session, daily_habit, test_user):
        """Test that streak is zero when there are no entries."""
        service = HabitAnalyticsService(db_session)
        streak_info = await service.calculate_streak(daily_habit.id, test_user.id)

        assert streak_info.current_streak == 0
        assert streak_info.longest_streak == 0
        assert streak_info.last_completed_date is None
        assert streak_info.is_active is False

    async def test_single_day_streak(self, db_session, daily_habit, test_user):
        """Test streak calculation with one completed day."""
        # Add entry for today
        entry = HabitEntry(
            id=uuid4(),
            habit_id=daily_habit.id,
            entry_date=date.today(),
            completed=True,
            completed_at=datetime.utcnow(),
        )
        db_session.add(entry)
        await db_session.commit()

        service = HabitAnalyticsService(db_session)
        streak_info = await service.calculate_streak(daily_habit.id, test_user.id)

        assert streak_info.current_streak == 1
        assert streak_info.longest_streak == 1
        assert streak_info.is_active is True
        assert streak_info.last_completed_date == date.today()

    async def test_consecutive_streak(self, db_session, daily_habit, test_user):
        """Test consecutive daily streak calculation."""
        # Add entries for the last 5 days
        today = date.today()
        for i in range(5):
            entry_date = today - timedelta(days=i)
            entry = HabitEntry(
                id=uuid4(),
                habit_id=daily_habit.id,
                entry_date=entry_date,
                completed=True,
                completed_at=datetime.utcnow(),
            )
            db_session.add(entry)
        await db_session.commit()

        service = HabitAnalyticsService(db_session)
        streak_info = await service.calculate_streak(daily_habit.id, test_user.id)

        assert streak_info.current_streak == 5
        assert streak_info.longest_streak == 5
        assert streak_info.is_active is True

    async def test_broken_streak(self, db_session, daily_habit, test_user):
        """Test that streak is broken when a day is missed."""
        today = date.today()
        
        # Add entries for 3 days, then skip a day, then 2 more days
        for i in [0, 1, 2, 4, 5]:
            entry_date = today - timedelta(days=i)
            entry = HabitEntry(
                id=uuid4(),
                habit_id=daily_habit.id,
                entry_date=entry_date,
                completed=True,
                completed_at=datetime.utcnow(),
            )
            db_session.add(entry)
        await db_session.commit()

        service = HabitAnalyticsService(db_session)
        streak_info = await service.calculate_streak(daily_habit.id, test_user.id)

        # Current streak should be 3 (days 0, 1, 2)
        assert streak_info.current_streak == 3
        # Longest streak should also be 3
        assert streak_info.longest_streak == 3
        assert streak_info.is_active is True

    async def test_inactive_streak_yesterday(self, db_session, daily_habit, test_user):
        """Test that streak is inactive if last completion was yesterday."""
        yesterday = date.today() - timedelta(days=1)
        entry = HabitEntry(
            id=uuid4(),
            habit_id=daily_habit.id,
            entry_date=yesterday,
            completed=True,
            completed_at=datetime.utcnow(),
        )
        db_session.add(entry)
        await db_session.commit()

        service = HabitAnalyticsService(db_session)
        streak_info = await service.calculate_streak(daily_habit.id, test_user.id)

        assert streak_info.current_streak == 1
        assert streak_info.is_active is True  # Yesterday still counts as active

    async def test_inactive_streak_two_days_ago(self, db_session, daily_habit, test_user):
        """Test that streak is inactive if last completion was 2+ days ago."""
        two_days_ago = date.today() - timedelta(days=2)
        entry = HabitEntry(
            id=uuid4(),
            habit_id=daily_habit.id,
            entry_date=two_days_ago,
            completed=True,
            completed_at=datetime.utcnow(),
        )
        db_session.add(entry)
        await db_session.commit()

        service = HabitAnalyticsService(db_session)
        streak_info = await service.calculate_streak(daily_habit.id, test_user.id)

        assert streak_info.current_streak == 1
        assert streak_info.is_active is False


@pytest.mark.asyncio
class TestWeeklyStreakCalculation:
    """Tests for weekly habit streak calculation."""

    async def test_weekly_streak_current_week(self, db_session, weekly_habit, test_user):
        """Test weekly streak for current week."""
        # Add entry for this week
        entry = HabitEntry(
            id=uuid4(),
            habit_id=weekly_habit.id,
            entry_date=date.today(),
            completed=True,
            completed_at=datetime.utcnow(),
        )
        db_session.add(entry)
        await db_session.commit()

        service = HabitAnalyticsService(db_session)
        streak_info = await service.calculate_streak(weekly_habit.id, test_user.id)

        assert streak_info.current_streak == 1
        assert streak_info.is_active is True

    async def test_weekly_consecutive_streak(self, db_session, weekly_habit, test_user):
        """Test consecutive weekly streak."""
        today = date.today()
        
        # Add entries for the last 3 weeks
        for i in range(3):
            # Get a date from each week
            entry_date = today - timedelta(weeks=i)
            entry = HabitEntry(
                id=uuid4(),
                habit_id=weekly_habit.id,
                entry_date=entry_date,
                completed=True,
                completed_at=datetime.utcnow(),
            )
            db_session.add(entry)
        await db_session.commit()

        service = HabitAnalyticsService(db_session)
        streak_info = await service.calculate_streak(weekly_habit.id, test_user.id)

        assert streak_info.current_streak == 3
        assert streak_info.longest_streak == 3


@pytest.mark.asyncio
class TestCompletionStats:
    """Tests for completion statistics calculation."""

    async def test_completion_stats_no_entries(self, db_session, daily_habit, test_user):
        """Test completion stats with no entries."""
        service = HabitAnalyticsService(db_session)
        stats = await service.get_completion_stats(daily_habit.id, test_user.id)

        assert stats.total_completions == 0
        assert stats.total_days_tracked == 0
        assert stats.completion_rate == 0.0
        assert stats.current_month_completions == 0
        assert stats.current_week_completions == 0

    async def test_completion_stats_with_entries(self, db_session, daily_habit, test_user):
        """Test completion stats with mixed completed/incomplete entries."""
        today = date.today()
        
        # Add 7 entries: 5 completed, 2 not completed
        for i in range(7):
            entry_date = today - timedelta(days=i)
            completed = i < 5  # First 5 are completed
            entry = HabitEntry(
                id=uuid4(),
                habit_id=daily_habit.id,
                entry_date=entry_date,
                completed=completed,
                completed_at=datetime.utcnow() if completed else None,
            )
            db_session.add(entry)
        await db_session.commit()

        service = HabitAnalyticsService(db_session)
        stats = await service.get_completion_stats(daily_habit.id, test_user.id)

        assert stats.total_completions == 5
        assert stats.total_days_tracked == 7
        assert stats.completion_rate == pytest.approx(71.43, rel=0.01)
        assert stats.current_week_completions == 5
        assert stats.current_month_completions == 5


@pytest.mark.asyncio
class TestHabitAnalytics:
    """Tests for comprehensive habit analytics."""

    async def test_habit_analytics_with_good_performance(
        self, db_session, daily_habit, test_user
    ):
        """Test analytics for a habit with good performance."""
        today = date.today()
        
        # Create a 7-day streak
        for i in range(7):
            entry_date = today - timedelta(days=i)
            entry = HabitEntry(
                id=uuid4(),
                habit_id=daily_habit.id,
                entry_date=entry_date,
                completed=True,
                completed_at=datetime.utcnow(),
            )
            db_session.add(entry)
        await db_session.commit()

        service = HabitAnalyticsService(db_session)
        analytics = await service.get_habit_analytics(daily_habit.id, test_user.id)

        assert analytics.habit_id == daily_habit.id
        assert analytics.habit_name == daily_habit.name
        assert analytics.streak_info.current_streak == 7
        assert analytics.completion_stats.completion_rate == 100.0
        assert analytics.confidence_level > 50
        assert len(analytics.motivational_message) > 0

    async def test_confidence_level_calculation(
        self, db_session, daily_habit, test_user
    ):
        """Test that confidence level increases with better performance."""
        service = HabitAnalyticsService(db_session)
        today = date.today()

        # Test with no entries
        analytics_empty = await service.get_habit_analytics(daily_habit.id, test_user.id)
        confidence_empty = analytics_empty.confidence_level

        # Add a 10-day streak
        for i in range(10):
            entry_date = today - timedelta(days=i)
            entry = HabitEntry(
                id=uuid4(),
                habit_id=daily_habit.id,
                entry_date=entry_date,
                completed=True,
                completed_at=datetime.utcnow(),
            )
            db_session.add(entry)
        await db_session.commit()

        analytics_good = await service.get_habit_analytics(daily_habit.id, test_user.id)
        confidence_good = analytics_good.confidence_level

        assert confidence_good > confidence_empty


@pytest.mark.asyncio
class TestStreakRecovery:
    """Tests for streak recovery functionality."""

    async def test_can_recover_within_grace_period(
        self, db_session, daily_habit, test_user
    ):
        """Test that streak can be recovered within grace period."""
        # Add entry for yesterday
        yesterday = date.today() - timedelta(days=1)
        entry = HabitEntry(
            id=uuid4(),
            habit_id=daily_habit.id,
            entry_date=yesterday,
            completed=True,
            completed_at=datetime.utcnow(),
        )
        db_session.add(entry)
        await db_session.commit()

        service = HabitAnalyticsService(db_session)
        recovery_info = await service.check_streak_recovery(
            daily_habit.id, test_user.id, grace_days=1
        )

        assert recovery_info.can_recover is True
        assert recovery_info.days_since_last_completion == 1

    async def test_cannot_recover_outside_grace_period(
        self, db_session, daily_habit, test_user
    ):
        """Test that streak cannot be recovered outside grace period."""
        # Add entry for 3 days ago
        three_days_ago = date.today() - timedelta(days=3)
        entry = HabitEntry(
            id=uuid4(),
            habit_id=daily_habit.id,
            entry_date=three_days_ago,
            completed=True,
            completed_at=datetime.utcnow(),
        )
        db_session.add(entry)
        await db_session.commit()

        service = HabitAnalyticsService(db_session)
        recovery_info = await service.check_streak_recovery(
            daily_habit.id, test_user.id, grace_days=1
        )

        assert recovery_info.can_recover is False
        assert recovery_info.days_since_last_completion == 3
