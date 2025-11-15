"""
Generic repository for simple CRUD operations on all models.
"""

from typing import List, Optional
from uuid import UUID
from datetime import date

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.habit import Habit, HabitEntry
from app.models.food import Food
from app.models.workout import Workout
from app.models.daily_review import DailyReview
from app.models.blog_entry import BlogEntry
from app.models.progress_snapshot import ProgressSnapshot
from app.repositories.base_repository import BaseRepository


class HabitRepository(BaseRepository[Habit]):
    """Repository for habit operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(db, Habit)

    async def get_user_habits(
        self,
        user_id: UUID,
        is_active: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Habit]:
        """Get all habits for a user with optional filters."""
        query = select(Habit).where(Habit.user_id == user_id)

        if is_active is not None:
            query = query.where(Habit.is_active == is_active)

        query = query.offset(skip).limit(limit).order_by(Habit.created_at.desc())

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def count_user_habits(
        self, user_id: UUID, is_active: Optional[bool] = None
    ) -> int:
        """Count habits for a user."""
        query = select(Habit).where(Habit.user_id == user_id)
        if is_active is not None:
            query = query.where(Habit.is_active == is_active)
        result = await self.db.execute(query)
        return len(list(result.scalars().all()))


class HabitEntryRepository(BaseRepository[HabitEntry]):
    """Repository for habit entry operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(db, HabitEntry)

    async def get_habit_entries(
        self, habit_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[HabitEntry]:
        """Get all entries for a habit."""
        result = await self.db.execute(
            select(HabitEntry)
            .where(HabitEntry.habit_id == habit_id)
            .order_by(HabitEntry.entry_date.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_entry_by_date(
        self, habit_id: UUID, entry_date: date
    ) -> Optional[HabitEntry]:
        """Get habit entry by date."""
        result = await self.db.execute(
            select(HabitEntry).where(
                and_(
                    HabitEntry.habit_id == habit_id, HabitEntry.entry_date == entry_date
                )
            )
        )
        return result.scalar_one_or_none()


class FoodRepository(BaseRepository[Food]):
    """Repository for food operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(db, Food)

    async def get_user_foods(
        self,
        user_id: UUID,
        meal_type: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Food]:
        """Get all food entries for a user with optional filters."""
        query = select(Food).where(Food.user_id == user_id)

        if meal_type:
            query = query.where(Food.meal_type == meal_type)
        if start_date:
            query = query.where(Food.meal_date >= start_date)
        if end_date:
            query = query.where(Food.meal_date <= end_date)

        query = (
            query.offset(skip)
            .limit(limit)
            .order_by(Food.meal_date.desc(), Food.meal_time.desc())
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def count_user_foods(self, user_id: UUID) -> int:
        """Count food entries for a user."""
        result = await self.db.execute(select(Food).where(Food.user_id == user_id))
        return len(list(result.scalars().all()))


class WorkoutRepository(BaseRepository[Workout]):
    """Repository for workout operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(db, Workout)

    async def get_user_workouts(
        self,
        user_id: UUID,
        workout_type: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Workout]:
        """Get all workouts for a user with optional filters."""
        query = (
            select(Workout)
            .where(Workout.user_id == user_id)
            .options(selectinload(Workout.exercises))
        )

        if workout_type:
            query = query.where(Workout.workout_type == workout_type)
        if start_date:
            query = query.where(Workout.workout_date >= start_date)
        if end_date:
            query = query.where(Workout.workout_date <= end_date)

        query = query.offset(skip).limit(limit).order_by(Workout.workout_date.desc())

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def count_user_workouts(self, user_id: UUID) -> int:
        """Count workouts for a user."""
        result = await self.db.execute(
            select(Workout).where(Workout.user_id == user_id)
        )
        return len(list(result.scalars().all()))


class DailyReviewRepository(BaseRepository[DailyReview]):
    """Repository for daily review operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(db, DailyReview)

    async def get_user_reviews(
        self,
        user_id: UUID,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[DailyReview]:
        """Get all daily reviews for a user with optional filters."""
        query = select(DailyReview).where(DailyReview.user_id == user_id)

        if start_date:
            query = query.where(DailyReview.review_date >= start_date)
        if end_date:
            query = query.where(DailyReview.review_date <= end_date)

        query = query.offset(skip).limit(limit).order_by(DailyReview.review_date.desc())

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_review_by_date(
        self, user_id: UUID, review_date: date
    ) -> Optional[DailyReview]:
        """Get daily review by date."""
        result = await self.db.execute(
            select(DailyReview).where(
                and_(
                    DailyReview.user_id == user_id,
                    DailyReview.review_date == review_date,
                )
            )
        )
        return result.scalar_one_or_none()

    async def count_user_reviews(self, user_id: UUID) -> int:
        """Count reviews for a user."""
        result = await self.db.execute(
            select(DailyReview).where(DailyReview.user_id == user_id)
        )
        return len(list(result.scalars().all()))


class BlogEntryRepository(BaseRepository[BlogEntry]):
    """Repository for blog entry operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(db, BlogEntry)

    async def get_user_blog_entries(
        self,
        user_id: UUID,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[BlogEntry]:
        """Get all blog entries for a user with optional filters."""
        query = select(BlogEntry).where(BlogEntry.user_id == user_id)

        if status:
            query = query.where(BlogEntry.status == status)

        query = query.offset(skip).limit(limit).order_by(BlogEntry.created_at.desc())

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def count_user_blog_entries(
        self, user_id: UUID, status: Optional[str] = None
    ) -> int:
        """Count blog entries for a user."""
        query = select(BlogEntry).where(BlogEntry.user_id == user_id)
        if status:
            query = query.where(BlogEntry.status == status)
        result = await self.db.execute(query)
        return len(list(result.scalars().all()))


class ProgressSnapshotRepository(BaseRepository[ProgressSnapshot]):
    """Repository for progress snapshot operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(db, ProgressSnapshot)

    async def get_user_snapshots(
        self,
        user_id: UUID,
        snapshot_type: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[ProgressSnapshot]:
        """Get all progress snapshots for a user with optional filters."""
        query = select(ProgressSnapshot).where(ProgressSnapshot.user_id == user_id)

        if snapshot_type:
            query = query.where(ProgressSnapshot.snapshot_type == snapshot_type)

        query = (
            query.offset(skip)
            .limit(limit)
            .order_by(ProgressSnapshot.snapshot_date.desc())
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def count_user_snapshots(self, user_id: UUID) -> int:
        """Count snapshots for a user."""
        result = await self.db.execute(
            select(ProgressSnapshot).where(ProgressSnapshot.user_id == user_id)
        )
        return len(list(result.scalars().all()))
