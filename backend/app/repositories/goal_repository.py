"""
Goal repository for database operations.
"""

from typing import List, Optional
from uuid import UUID
from datetime import date

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.goal import Goal, GoalProgress, GoalMilestone
from app.repositories.base_repository import BaseRepository


class GoalRepository(BaseRepository[Goal]):
    """Repository for goal operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(db, Goal)

    async def get_user_goals(
        self,
        user_id: UUID,
        goal_type: Optional[str] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Goal]:
        """Get all goals for a user with optional filters."""
        query = select(Goal).where(Goal.user_id == user_id)

        if goal_type:
            query = query.where(Goal.goal_type == goal_type)
        if status:
            query = query.where(Goal.status == status)

        query = query.offset(skip).limit(limit).order_by(Goal.created_at.desc())

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_goals_by_date_range(
        self, user_id: UUID, start_date: date, end_date: date
    ) -> List[Goal]:
        """Get goals within a date range."""
        result = await self.db.execute(
            select(Goal)
            .where(
                and_(
                    Goal.user_id == user_id,
                    Goal.start_date <= end_date,
                    Goal.end_date >= start_date,
                )
            )
            .order_by(Goal.start_date)
        )
        return list(result.scalars().all())

    async def count_user_goals(
        self, user_id: UUID, status: Optional[str] = None
    ) -> int:
        """Count goals for a user."""
        query = select(Goal).where(Goal.user_id == user_id)
        if status:
            query = query.where(Goal.status == status)
        result = await self.db.execute(query)
        return len(list(result.scalars().all()))


class GoalProgressRepository(BaseRepository[GoalProgress]):
    """Repository for goal progress operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(db, GoalProgress)

    async def get_goal_progress(
        self, goal_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[GoalProgress]:
        """Get all progress entries for a goal."""
        result = await self.db.execute(
            select(GoalProgress)
            .where(GoalProgress.goal_id == goal_id)
            .order_by(GoalProgress.progress_date.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_latest_progress(self, goal_id: UUID) -> Optional[GoalProgress]:
        """Get the latest progress entry for a goal."""
        result = await self.db.execute(
            select(GoalProgress)
            .where(GoalProgress.goal_id == goal_id)
            .order_by(GoalProgress.progress_date.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()


class GoalMilestoneRepository(BaseRepository[GoalMilestone]):
    """Repository for goal milestone operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(db, GoalMilestone)

    async def get_goal_milestones(
        self, goal_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[GoalMilestone]:
        """Get all milestones for a goal."""
        result = await self.db.execute(
            select(GoalMilestone)
            .where(GoalMilestone.goal_id == goal_id)
            .order_by(GoalMilestone.order_index.asc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def count_completed_milestones(self, goal_id: UUID) -> int:
        """Count completed milestones for a goal."""
        result = await self.db.execute(
            select(GoalMilestone).where(
                and_(
                    GoalMilestone.goal_id == goal_id,
                    GoalMilestone.status == "completed",
                )
            )
        )
        return len(list(result.scalars().all()))
