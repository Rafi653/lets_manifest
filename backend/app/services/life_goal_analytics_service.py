"""
Life goals analytics service for reporting and statistics.
"""

from datetime import datetime, timedelta
from typing import Dict, List
from uuid import UUID

from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.goal import Goal, GoalMilestone


class LifeGoalAnalyticsService:
    """Service for life goal analytics and reporting."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_life_goals_summary(self, user_id: UUID) -> Dict:
        """Get summary statistics for user's life goals."""

        # Get all life goals
        result = await self.db.execute(
            select(Goal).where(
                and_(Goal.user_id == user_id, Goal.goal_type == "life_goal")
            )
        )
        life_goals = list(result.scalars().all())

        total_goals = len(life_goals)
        active_goals = len(
            [g for g in life_goals if g.status == "active" or g.status == "in_progress"]
        )
        completed_goals = len([g for g in life_goals if g.status == "completed"])

        # Get goals by category
        goals_by_category = {}
        for goal in life_goals:
            category = goal.category or "uncategorized"
            if category not in goals_by_category:
                goals_by_category[category] = 0
            goals_by_category[category] += 1

        # Calculate completion rate
        completion_rate = (
            (completed_goals / total_goals * 100) if total_goals > 0 else 0
        )

        # Get average time to completion
        completed_with_dates = [
            g
            for g in life_goals
            if g.status == "completed" and g.created_at and g.completed_at
        ]
        avg_days_to_complete = None
        if completed_with_dates:
            total_days = sum(
                [(g.completed_at - g.created_at).days for g in completed_with_dates]
            )
            avg_days_to_complete = total_days / len(completed_with_dates)

        return {
            "total_goals": total_goals,
            "active_goals": active_goals,
            "completed_goals": completed_goals,
            "cancelled_goals": len([g for g in life_goals if g.status == "cancelled"]),
            "completion_rate": round(completion_rate, 2),
            "goals_by_category": goals_by_category,
            "avg_days_to_complete": (
                round(avg_days_to_complete, 1) if avg_days_to_complete else None
            ),
        }

    async def get_milestone_statistics(
        self, user_id: UUID, goal_id: UUID = None
    ) -> Dict:
        """Get milestone statistics for a specific goal or all user's life goals."""

        # Build query
        if goal_id:
            # Get milestones for specific goal
            goal_result = await self.db.execute(
                select(Goal).where(and_(Goal.id == goal_id, Goal.user_id == user_id))
            )
            goal = goal_result.scalar_one_or_none()
            if not goal:
                return {}

            milestone_result = await self.db.execute(
                select(GoalMilestone).where(GoalMilestone.goal_id == goal_id)
            )
            milestones = list(milestone_result.scalars().all())
        else:
            # Get milestones for all user's life goals
            goal_ids_result = await self.db.execute(
                select(Goal.id).where(
                    and_(Goal.user_id == user_id, Goal.goal_type == "life_goal")
                )
            )
            goal_ids = [row[0] for row in goal_ids_result.all()]

            if not goal_ids:
                return {
                    "total_milestones": 0,
                    "completed_milestones": 0,
                    "in_progress_milestones": 0,
                    "pending_milestones": 0,
                    "completion_rate": 0,
                }

            milestone_result = await self.db.execute(
                select(GoalMilestone).where(GoalMilestone.goal_id.in_(goal_ids))
            )
            milestones = list(milestone_result.scalars().all())

        total = len(milestones)
        completed = len([m for m in milestones if m.status == "completed"])
        in_progress = len([m for m in milestones if m.status == "in_progress"])
        pending = len([m for m in milestones if m.status == "pending"])

        completion_rate = (completed / total * 100) if total > 0 else 0

        return {
            "total_milestones": total,
            "completed_milestones": completed,
            "in_progress_milestones": in_progress,
            "pending_milestones": pending,
            "skipped_milestones": len([m for m in milestones if m.status == "skipped"]),
            "completion_rate": round(completion_rate, 2),
        }

    async def get_goals_by_life_area(self, user_id: UUID) -> List[Dict]:
        """Get life goals grouped by life area/category."""

        result = await self.db.execute(
            select(Goal)
            .where(and_(Goal.user_id == user_id, Goal.goal_type == "life_goal"))
            .order_by(Goal.category, Goal.created_at.desc())
        )
        life_goals = list(result.scalars().all())

        # Group by category
        categorized = {}
        for goal in life_goals:
            category = goal.category or "uncategorized"
            if category not in categorized:
                categorized[category] = []

            categorized[category].append(
                {
                    "id": str(goal.id),
                    "title": goal.title,
                    "status": goal.status,
                    "priority": goal.priority,
                    "created_at": (
                        goal.created_at.isoformat() if goal.created_at else None
                    ),
                    "completed_at": (
                        goal.completed_at.isoformat() if goal.completed_at else None
                    ),
                }
            )

        # Convert to list format
        result_list = []
        for category, goals in categorized.items():
            result_list.append(
                {"life_area": category, "goal_count": len(goals), "goals": goals}
            )

        return result_list
