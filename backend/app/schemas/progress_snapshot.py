"""
Progress snapshot-related Pydantic schemas.
"""

from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ProgressSnapshotBase(BaseModel):
    """Base schema for progress snapshot."""

    snapshot_date: date
    snapshot_type: str = Field(..., pattern="^(weekly|monthly|yearly)$")
    total_goals: int = Field(default=0, ge=0)
    completed_goals: int = Field(default=0, ge=0)
    active_habits: int = Field(default=0, ge=0)
    habit_completion_rate: Optional[Decimal] = Field(None, ge=0, le=100)
    total_workouts: int = Field(default=0, ge=0)
    total_workout_minutes: int = Field(default=0, ge=0)
    average_daily_mood: Optional[Decimal] = Field(None, ge=1, le=10)
    average_energy_level: Optional[Decimal] = Field(None, ge=1, le=10)
    total_blog_entries: int = Field(default=0, ge=0)
    weight: Optional[Decimal] = Field(None, ge=0)
    weight_unit: str = Field(default="lbs", pattern="^(lbs|kg)$")
    body_fat_percentage: Optional[Decimal] = Field(None, ge=0, le=100)
    notes: Optional[str] = None


class ProgressSnapshotCreate(ProgressSnapshotBase):
    """Schema for creating progress snapshot."""

    pass


class ProgressSnapshotUpdate(BaseModel):
    """Schema for updating progress snapshot."""

    total_goals: Optional[int] = Field(None, ge=0)
    completed_goals: Optional[int] = Field(None, ge=0)
    active_habits: Optional[int] = Field(None, ge=0)
    habit_completion_rate: Optional[Decimal] = Field(None, ge=0, le=100)
    total_workouts: Optional[int] = Field(None, ge=0)
    total_workout_minutes: Optional[int] = Field(None, ge=0)
    average_daily_mood: Optional[Decimal] = Field(None, ge=1, le=10)
    average_energy_level: Optional[Decimal] = Field(None, ge=1, le=10)
    total_blog_entries: Optional[int] = Field(None, ge=0)
    weight: Optional[Decimal] = Field(None, ge=0)
    weight_unit: Optional[str] = Field(None, pattern="^(lbs|kg)$")
    body_fat_percentage: Optional[Decimal] = Field(None, ge=0, le=100)
    notes: Optional[str] = None


class ProgressSnapshotResponse(ProgressSnapshotBase):
    """Schema for progress snapshot response."""

    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
