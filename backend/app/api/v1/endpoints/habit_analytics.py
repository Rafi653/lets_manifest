"""
Habit analytics endpoints.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.common import APIResponse
from app.schemas.habit_analytics import (
    HabitAnalytics,
    ProgressTrends,
    StreakRecoveryInfo,
    HabitInsights,
)
from app.services.habit_analytics_service import HabitAnalyticsService

router = APIRouter()


@router.get("/{habit_id}/analytics", response_model=APIResponse[HabitAnalytics])
async def get_habit_analytics(
    habit_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get comprehensive analytics for a habit including:
    - Streak information (current, longest, status)
    - Completion statistics
    - Confidence level
    - Motivational messages
    """
    service = HabitAnalyticsService(db)
    analytics = await service.get_habit_analytics(habit_id, current_user.id)
    return APIResponse(
        data=analytics,
        message="Habit analytics retrieved successfully",
    )


@router.get("/{habit_id}/progress", response_model=APIResponse[ProgressTrends])
async def get_habit_progress_trends(
    habit_id: UUID,
    days: int = Query(90, ge=7, le=365, description="Number of days to analyze"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get progress trends over time including:
    - Daily completion data
    - Weekly summaries
    - Monthly summaries
    - Overall trend direction
    """
    service = HabitAnalyticsService(db)
    trends = await service.get_progress_trends(habit_id, current_user.id, days)
    return APIResponse(
        data=trends,
        message="Progress trends retrieved successfully",
    )


@router.get(
    "/{habit_id}/streak-recovery", response_model=APIResponse[StreakRecoveryInfo]
)
async def check_streak_recovery(
    habit_id: UUID,
    grace_days: int = Query(
        1, ge=0, le=7, description="Grace period days for streak recovery"
    ),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Check if a broken streak can be recovered.
    Returns recovery information and deadlines.
    """
    service = HabitAnalyticsService(db)
    recovery_info = await service.check_streak_recovery(
        habit_id, current_user.id, grace_days
    )
    return APIResponse(
        data=recovery_info,
        message="Streak recovery info retrieved successfully",
    )


@router.get("/insights", response_model=APIResponse[HabitInsights])
async def get_user_habit_insights(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get aggregated insights across all user's habits including:
    - Best performing habits
    - Habits needing attention
    - Overall statistics
    - Motivational insights
    """
    service = HabitAnalyticsService(db)
    insights = await service.get_user_insights(current_user.id)
    return APIResponse(
        data=insights,
        message="Habit insights retrieved successfully",
    )
