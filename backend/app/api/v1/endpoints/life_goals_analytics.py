"""
Life goals analytics endpoints.
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.common import APIResponse
from app.services.life_goal_analytics_service import LifeGoalAnalyticsService

router = APIRouter()


@router.get("/life-goals/summary", response_model=APIResponse[dict])
async def get_life_goals_summary(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get summary statistics for user's life goals.

    Returns:
    - Total number of life goals
    - Active, completed, and cancelled goals count
    - Completion rate
    - Goals grouped by category/life area
    - Average time to completion
    """
    service = LifeGoalAnalyticsService(db)
    summary = await service.get_life_goals_summary(current_user.id)

    return APIResponse(
        data=summary, message="Life goals summary retrieved successfully"
    )


@router.get("/life-goals/milestones/statistics", response_model=APIResponse[dict])
async def get_milestone_statistics(
    goal_id: Optional[UUID] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get milestone statistics.

    If goal_id is provided, returns statistics for that specific goal.
    Otherwise, returns statistics across all user's life goals.

    Returns:
    - Total milestones
    - Completed, in progress, and pending counts
    - Milestone completion rate
    """
    service = LifeGoalAnalyticsService(db)
    stats = await service.get_milestone_statistics(current_user.id, goal_id)

    return APIResponse(
        data=stats, message="Milestone statistics retrieved successfully"
    )


@router.get("/life-goals/by-life-area", response_model=APIResponse[list])
async def get_goals_by_life_area(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get life goals grouped by life area/category.

    Returns goals organized by categories such as:
    - investment
    - travel
    - health
    - paperwork
    - career
    - relationships
    - personal_growth
    - etc.
    """
    service = LifeGoalAnalyticsService(db)
    goals_by_area = await service.get_goals_by_life_area(current_user.id)

    return APIResponse(
        data=goals_by_area, message="Goals by life area retrieved successfully"
    )
