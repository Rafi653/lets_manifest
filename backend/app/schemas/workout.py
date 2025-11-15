"""
Workout-related Pydantic schemas.
"""

from datetime import date, datetime, time
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class WorkoutExerciseBase(BaseModel):
    """Base schema for workout exercise."""

    exercise_name: str = Field(..., max_length=255)
    exercise_type: Optional[str] = Field(None, max_length=50)
    sets: Optional[int] = Field(None, ge=0)
    reps: Optional[int] = Field(None, ge=0)
    weight: Optional[Decimal] = Field(None, ge=0)
    weight_unit: str = Field(default="lbs", pattern="^(lbs|kg)$")
    distance: Optional[Decimal] = Field(None, ge=0)
    distance_unit: Optional[str] = Field(None, pattern="^(miles|km|meters)$")
    duration_seconds: Optional[int] = Field(None, ge=0)
    rest_seconds: Optional[int] = Field(None, ge=0)
    notes: Optional[str] = None
    order_index: int = Field(default=0, ge=0)


class WorkoutExerciseCreate(WorkoutExerciseBase):
    """Schema for creating workout exercise."""

    pass


class WorkoutExerciseResponse(WorkoutExerciseBase):
    """Schema for workout exercise response."""

    id: UUID
    workout_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class WorkoutBase(BaseModel):
    """Base schema for workout."""

    workout_date: date
    workout_time: Optional[time] = None
    workout_type: str = Field(..., max_length=50)
    workout_name: Optional[str] = Field(None, max_length=255)
    duration_minutes: Optional[int] = Field(None, ge=0)
    calories_burned: Optional[Decimal] = Field(None, ge=0)
    intensity: Optional[str] = Field(None, pattern="^(low|medium|high)$")
    location: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = None
    mood_before: Optional[str] = Field(None, max_length=20)
    mood_after: Optional[str] = Field(None, max_length=20)


class WorkoutCreate(WorkoutBase):
    """Schema for creating workout."""

    exercises: List[WorkoutExerciseCreate] = []


class WorkoutUpdate(BaseModel):
    """Schema for updating workout."""

    workout_time: Optional[time] = None
    workout_type: Optional[str] = Field(None, max_length=50)
    workout_name: Optional[str] = Field(None, max_length=255)
    duration_minutes: Optional[int] = Field(None, ge=0)
    calories_burned: Optional[Decimal] = Field(None, ge=0)
    intensity: Optional[str] = Field(None, pattern="^(low|medium|high)$")
    location: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = None
    mood_before: Optional[str] = Field(None, max_length=20)
    mood_after: Optional[str] = Field(None, max_length=20)


class WorkoutResponse(WorkoutBase):
    """Schema for workout response."""

    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    exercises: List[WorkoutExerciseResponse] = []

    class Config:
        from_attributes = True
