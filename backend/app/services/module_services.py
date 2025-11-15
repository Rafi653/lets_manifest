"""
Services for all app modules - habits, food, workouts, daily reviews, blog, progress.
"""

from datetime import datetime, date, timedelta
from typing import List, Optional
from uuid import UUID
import re

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.habit import Habit, HabitEntry
from app.models.food import Food
from app.models.workout import Workout, WorkoutExercise
from app.models.daily_review import DailyReview
from app.models.blog_entry import BlogEntry
from app.models.progress_snapshot import ProgressSnapshot
from app.repositories.module_repositories import (
    HabitRepository,
    HabitEntryRepository,
    FoodRepository,
    WorkoutRepository,
    DailyReviewRepository,
    BlogEntryRepository,
    ProgressSnapshotRepository,
)
from app.schemas.habit import (
    HabitCreate,
    HabitUpdate,
    HabitEntryCreate,
)
from app.schemas.food import FoodCreate, FoodUpdate
from app.schemas.workout import WorkoutCreate, WorkoutUpdate
from app.schemas.daily_review import DailyReviewCreate, DailyReviewUpdate
from app.schemas.blog_entry import BlogEntryCreate, BlogEntryUpdate
from app.schemas.progress_snapshot import ProgressSnapshotCreate, ProgressSnapshotUpdate


class HabitService:
    """Service for habit operations."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = HabitRepository(db)
        self.entry_repository = HabitEntryRepository(db)

    async def create_habit(self, user_id: UUID, habit_data: HabitCreate) -> Habit:
        """Create a new habit."""
        habit = Habit(user_id=user_id, **habit_data.model_dump())
        return await self.repository.create(habit)

    async def get_habit(self, habit_id: UUID, user_id: UUID) -> Habit:
        """Get a habit by ID."""
        habit = await self.repository.get_by_id(habit_id)
        if not habit or habit.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Habit not found"
            )
        return habit

    async def get_user_habits(
        self,
        user_id: UUID,
        is_active: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[List[Habit], int]:
        """Get all habits for a user."""
        habits = await self.repository.get_user_habits(user_id, is_active, skip, limit)
        total = await self.repository.count_user_habits(user_id, is_active)
        return habits, total

    async def update_habit(
        self, habit_id: UUID, user_id: UUID, habit_data: HabitUpdate
    ) -> Habit:
        """Update a habit."""
        habit = await self.get_habit(habit_id, user_id)
        update_data = habit_data.model_dump(exclude_unset=True)
        return await self.repository.update(habit, update_data)

    async def delete_habit(self, habit_id: UUID, user_id: UUID) -> bool:
        """Delete a habit."""
        await self.get_habit(habit_id, user_id)
        return await self.repository.delete(habit_id)

    async def create_entry(
        self, habit_id: UUID, user_id: UUID, entry_data: HabitEntryCreate
    ) -> HabitEntry:
        """Create a habit entry and update streaks."""
        habit = await self.get_habit(habit_id, user_id)

        # Check if entry already exists for this date
        existing = await self.entry_repository.get_entry_by_date(
            habit_id, entry_data.entry_date
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Entry already exists for this date",
            )

        entry = HabitEntry(
            habit_id=habit_id,
            **entry_data.model_dump(),
            completed_at=datetime.utcnow() if entry_data.completed else None
        )
        
        created_entry = await self.entry_repository.create(entry)

        # Update habit stats using analytics service
        if entry_data.completed:
            from app.services.habit_analytics_service import HabitAnalyticsService
            analytics_service = HabitAnalyticsService(self.db)
            streak_info = await analytics_service.calculate_streak(habit_id, user_id)
            
            habit.total_completions += 1
            habit.current_streak = streak_info.current_streak
            habit.longest_streak = streak_info.longest_streak
            await self.db.commit()

        return created_entry

    async def reset_habit_streak(self, habit_id: UUID, user_id: UUID) -> Habit:
        """Reset a habit's streak to zero."""
        habit = await self.get_habit(habit_id, user_id)
        habit.current_streak = 0
        await self.db.commit()
        await self.db.refresh(habit)
        return habit

    async def recover_streak(
        self, habit_id: UUID, user_id: UUID, recovery_date: date
    ) -> HabitEntry:
        """
        Recover a streak by creating an entry for a missed date.
        Only allowed within grace period.
        """
        from app.services.habit_analytics_service import HabitAnalyticsService
        analytics_service = HabitAnalyticsService(self.db)
        
        # Check if recovery is allowed
        recovery_info = await analytics_service.check_streak_recovery(habit_id, user_id)
        if not recovery_info.can_recover:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Streak recovery is no longer available for this habit",
            )

        # Check if entry already exists
        existing = await self.entry_repository.get_entry_by_date(habit_id, recovery_date)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Entry already exists for this date",
            )

        # Verify recovery date is within allowed range
        if recovery_date > date.today() or recovery_date < (date.today() - timedelta(days=recovery_info.grace_period_days + 1)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Recovery date is outside the allowed grace period",
            )

        # Create recovery entry
        entry = HabitEntry(
            habit_id=habit_id,
            entry_date=recovery_date,
            completed=True,
            completed_at=datetime.utcnow(),
            notes="Streak recovery"
        )
        
        created_entry = await self.entry_repository.create(entry)

        # Update habit stats
        habit = await self.get_habit(habit_id, user_id)
        habit.total_completions += 1
        
        # Recalculate streak
        streak_info = await analytics_service.calculate_streak(habit_id, user_id)
        habit.current_streak = streak_info.current_streak
        habit.longest_streak = streak_info.longest_streak
        
        await self.db.commit()
        return created_entry

    async def get_habit_entries(
        self, habit_id: UUID, user_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[HabitEntry]:
        """Get entries for a habit."""
        await self.get_habit(habit_id, user_id)
        return await self.entry_repository.get_habit_entries(habit_id, skip, limit)


class FoodService:
    """Service for food tracking operations."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = FoodRepository(db)

    async def create_food(self, user_id: UUID, food_data: FoodCreate) -> Food:
        """Create a food entry."""
        food = Food(user_id=user_id, **food_data.model_dump())
        return await self.repository.create(food)

    async def get_food(self, food_id: UUID, user_id: UUID) -> Food:
        """Get a food entry by ID."""
        food = await self.repository.get_by_id(food_id)
        if not food or food.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Food entry not found"
            )
        return food

    async def get_user_foods(
        self,
        user_id: UUID,
        meal_type: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[List[Food], int]:
        """Get all food entries for a user."""
        foods = await self.repository.get_user_foods(
            user_id, meal_type, start_date, end_date, skip, limit
        )
        total = await self.repository.count_user_foods(user_id)
        return foods, total

    async def update_food(
        self, food_id: UUID, user_id: UUID, food_data: FoodUpdate
    ) -> Food:
        """Update a food entry."""
        food = await self.get_food(food_id, user_id)
        update_data = food_data.model_dump(exclude_unset=True)
        return await self.repository.update(food, update_data)

    async def delete_food(self, food_id: UUID, user_id: UUID) -> bool:
        """Delete a food entry."""
        await self.get_food(food_id, user_id)
        return await self.repository.delete(food_id)


class WorkoutService:
    """Service for workout operations."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = WorkoutRepository(db)

    async def create_workout(
        self, user_id: UUID, workout_data: WorkoutCreate
    ) -> Workout:
        """Create a workout with exercises."""
        workout = Workout(
            user_id=user_id, **workout_data.model_dump(exclude={"exercises"})
        )
        workout = await self.repository.create(workout)

        # Create exercises
        for i, exercise_data in enumerate(workout_data.exercises):
            exercise = WorkoutExercise(
                workout_id=workout.id, **exercise_data.model_dump()
            )
            self.db.add(exercise)

        await self.db.flush()
        await self.db.refresh(workout)
        return workout

    async def get_workout(self, workout_id: UUID, user_id: UUID) -> Workout:
        """Get a workout by ID."""
        workout = await self.repository.get_by_id(workout_id)
        if not workout or workout.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Workout not found"
            )
        return workout

    async def get_user_workouts(
        self,
        user_id: UUID,
        workout_type: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[List[Workout], int]:
        """Get all workouts for a user."""
        workouts = await self.repository.get_user_workouts(
            user_id, workout_type, start_date, end_date, skip, limit
        )
        total = await self.repository.count_user_workouts(user_id)
        return workouts, total

    async def update_workout(
        self, workout_id: UUID, user_id: UUID, workout_data: WorkoutUpdate
    ) -> Workout:
        """Update a workout."""
        workout = await self.get_workout(workout_id, user_id)
        update_data = workout_data.model_dump(exclude_unset=True)
        return await self.repository.update(workout, update_data)

    async def delete_workout(self, workout_id: UUID, user_id: UUID) -> bool:
        """Delete a workout."""
        await self.get_workout(workout_id, user_id)
        return await self.repository.delete(workout_id)


class DailyReviewService:
    """Service for daily review operations."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = DailyReviewRepository(db)

    async def create_review(
        self, user_id: UUID, review_data: DailyReviewCreate
    ) -> DailyReview:
        """Create a daily review."""
        # Check if review already exists for this date
        existing = await self.repository.get_review_by_date(
            user_id, review_data.review_date
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Review already exists for this date",
            )

        review = DailyReview(user_id=user_id, **review_data.model_dump())
        return await self.repository.create(review)

    async def get_review(self, review_id: UUID, user_id: UUID) -> DailyReview:
        """Get a daily review by ID."""
        review = await self.repository.get_by_id(review_id)
        if not review or review.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Daily review not found"
            )
        return review

    async def get_user_reviews(
        self,
        user_id: UUID,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[List[DailyReview], int]:
        """Get all daily reviews for a user."""
        reviews = await self.repository.get_user_reviews(
            user_id, start_date, end_date, skip, limit
        )
        total = await self.repository.count_user_reviews(user_id)
        return reviews, total

    async def update_review(
        self, review_id: UUID, user_id: UUID, review_data: DailyReviewUpdate
    ) -> DailyReview:
        """Update a daily review."""
        review = await self.get_review(review_id, user_id)
        update_data = review_data.model_dump(exclude_unset=True)
        return await self.repository.update(review, update_data)

    async def delete_review(self, review_id: UUID, user_id: UUID) -> bool:
        """Delete a daily review."""
        await self.get_review(review_id, user_id)
        return await self.repository.delete(review_id)


class BlogEntryService:
    """Service for blog entry operations."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = BlogEntryRepository(db)

    def _generate_slug(self, title: str) -> str:
        """Generate a URL-friendly slug from title."""
        slug = title.lower()
        slug = re.sub(r"[^a-z0-9]+", "-", slug)
        slug = slug.strip("-")
        return slug[:200]  # Limit length

    async def create_blog_entry(
        self, user_id: UUID, entry_data: BlogEntryCreate
    ) -> BlogEntry:
        """Create a blog entry."""
        slug = self._generate_slug(entry_data.title)

        entry = BlogEntry(
            user_id=user_id,
            slug=slug,
            **entry_data.model_dump(),
            published_at=datetime.utcnow() if entry_data.status == "published" else None
        )
        return await self.repository.create(entry)

    async def get_blog_entry(self, entry_id: UUID, user_id: UUID) -> BlogEntry:
        """Get a blog entry by ID."""
        entry = await self.repository.get_by_id(entry_id)
        if not entry or entry.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Blog entry not found"
            )
        return entry

    async def get_user_blog_entries(
        self,
        user_id: UUID,
        status_filter: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[List[BlogEntry], int]:
        """Get all blog entries for a user."""
        entries = await self.repository.get_user_blog_entries(
            user_id, status_filter, skip, limit
        )
        total = await self.repository.count_user_blog_entries(user_id, status_filter)
        return entries, total

    async def update_blog_entry(
        self, entry_id: UUID, user_id: UUID, entry_data: BlogEntryUpdate
    ) -> BlogEntry:
        """Update a blog entry."""
        entry = await self.get_blog_entry(entry_id, user_id)
        update_data = entry_data.model_dump(exclude_unset=True)

        # Update slug if title changed
        if "title" in update_data:
            update_data["slug"] = self._generate_slug(update_data["title"])

        # Set published_at if status changed to published
        if update_data.get("status") == "published" and not entry.published_at:
            update_data["published_at"] = datetime.utcnow()

        return await self.repository.update(entry, update_data)

    async def delete_blog_entry(self, entry_id: UUID, user_id: UUID) -> bool:
        """Delete a blog entry."""
        await self.get_blog_entry(entry_id, user_id)
        return await self.repository.delete(entry_id)


class ProgressSnapshotService:
    """Service for progress snapshot operations."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = ProgressSnapshotRepository(db)

    async def create_snapshot(
        self, user_id: UUID, snapshot_data: ProgressSnapshotCreate
    ) -> ProgressSnapshot:
        """Create a progress snapshot."""
        snapshot = ProgressSnapshot(user_id=user_id, **snapshot_data.model_dump())
        return await self.repository.create(snapshot)

    async def get_snapshot(self, snapshot_id: UUID, user_id: UUID) -> ProgressSnapshot:
        """Get a progress snapshot by ID."""
        snapshot = await self.repository.get_by_id(snapshot_id)
        if not snapshot or snapshot.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Progress snapshot not found",
            )
        return snapshot

    async def get_user_snapshots(
        self,
        user_id: UUID,
        snapshot_type: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[List[ProgressSnapshot], int]:
        """Get all progress snapshots for a user."""
        snapshots = await self.repository.get_user_snapshots(
            user_id, snapshot_type, skip, limit
        )
        total = await self.repository.count_user_snapshots(user_id)
        return snapshots, total

    async def update_snapshot(
        self, snapshot_id: UUID, user_id: UUID, snapshot_data: ProgressSnapshotUpdate
    ) -> ProgressSnapshot:
        """Update a progress snapshot."""
        snapshot = await self.get_snapshot(snapshot_id, user_id)
        update_data = snapshot_data.model_dump(exclude_unset=True)
        return await self.repository.update(snapshot, update_data)

    async def delete_snapshot(self, snapshot_id: UUID, user_id: UUID) -> bool:
        """Delete a progress snapshot."""
        await self.get_snapshot(snapshot_id, user_id)
        return await self.repository.delete(snapshot_id)
