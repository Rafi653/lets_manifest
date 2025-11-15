"""
Schemas for habit analytics and streak tracking.
"""

from datetime import date, datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class StreakInfo(BaseModel):
    """Information about a habit streak."""

    current_streak: int = Field(ge=0, description="Current consecutive completion streak")
    longest_streak: int = Field(ge=0, description="Longest streak ever achieved")
    last_completed_date: Optional[date] = Field(
        None, description="Date of last completion"
    )
    is_active: bool = Field(
        description="Whether the streak is currently active (completed today/this period)"
    )
    streak_start_date: Optional[date] = Field(
        None, description="Date when current streak started"
    )


class CompletionStats(BaseModel):
    """Habit completion statistics."""

    total_completions: int = Field(ge=0, description="Total number of completions")
    total_days_tracked: int = Field(
        ge=0, description="Total number of days with entries"
    )
    completion_rate: float = Field(
        ge=0, le=100, description="Completion rate percentage"
    )
    current_month_completions: int = Field(
        ge=0, description="Completions in current month"
    )
    current_week_completions: int = Field(
        ge=0, description="Completions in current week"
    )


class HabitAnalytics(BaseModel):
    """Comprehensive habit analytics."""

    habit_id: UUID
    habit_name: str
    frequency: str
    streak_info: StreakInfo
    completion_stats: CompletionStats
    confidence_level: int = Field(
        ge=0, le=100, description="Confidence level based on consistency (0-100)"
    )
    motivational_message: str = Field(description="Personalized motivational message")


class DailyCompletionData(BaseModel):
    """Daily completion data for visualization."""

    date: date
    completed: bool
    mood: Optional[str] = None
    notes: Optional[str] = None


class WeeklyProgress(BaseModel):
    """Weekly progress summary."""

    week_start: date
    week_end: date
    completions: int
    target: int
    completion_rate: float


class MonthlyProgress(BaseModel):
    """Monthly progress summary."""

    month: int
    year: int
    completions: int
    target: int
    completion_rate: float


class ProgressTrends(BaseModel):
    """Progress trends over time."""

    daily_data: List[DailyCompletionData] = Field(
        description="Daily completion data for the past period"
    )
    weekly_summaries: List[WeeklyProgress] = Field(
        description="Weekly progress summaries"
    )
    monthly_summaries: List[MonthlyProgress] = Field(
        description="Monthly progress summaries"
    )
    overall_trend: str = Field(
        description="Overall trend direction: improving, stable, declining"
    )


class StreakRecoveryInfo(BaseModel):
    """Information about streak recovery options."""

    can_recover: bool = Field(description="Whether streak can be recovered")
    days_since_last_completion: int = Field(description="Days since last completion")
    recovery_deadline: Optional[date] = Field(
        None, description="Last date to recover streak"
    )
    grace_period_days: int = Field(
        default=1, description="Grace period for streak recovery"
    )


class HabitInsights(BaseModel):
    """Aggregated insights and recommendations."""

    best_performing_habits: List[str] = Field(
        description="Names of habits with highest completion rates"
    )
    needs_attention: List[str] = Field(
        description="Names of habits that need more attention"
    )
    total_active_streaks: int = Field(description="Number of currently active streaks")
    average_streak_length: float = Field(description="Average streak length across all habits")
    overall_completion_rate: float = Field(
        description="Overall completion rate across all habits"
    )
    motivational_insights: List[str] = Field(
        description="Personalized motivational insights"
    )
