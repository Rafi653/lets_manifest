"""
Habit-related Pydantic schemas.
"""

from datetime import date, datetime, time
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class HabitBase(BaseModel):
    """Base schema for habit."""

    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    frequency: str = Field(..., pattern="^(daily|weekly|custom)$")
    target_days: Optional[int] = Field(None, ge=1, le=7)
    category: Optional[str] = Field(None, max_length=50)
    color: Optional[str] = Field(None, max_length=7)
    icon: Optional[str] = Field(None, max_length=50)
    reminder_time: Optional[time] = None


class HabitCreate(HabitBase):
    """Schema for creating a habit."""

    pass


class HabitUpdate(BaseModel):
    """Schema for updating a habit."""

    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    frequency: Optional[str] = Field(None, pattern="^(daily|weekly|custom)$")
    target_days: Optional[int] = Field(None, ge=1, le=7)
    category: Optional[str] = Field(None, max_length=50)
    color: Optional[str] = Field(None, max_length=7)
    icon: Optional[str] = Field(None, max_length=50)
    reminder_time: Optional[time] = None
    is_active: Optional[bool] = None


class HabitResponse(HabitBase):
    """Schema for habit response."""

    id: UUID
    user_id: UUID
    is_active: bool
    current_streak: int
    longest_streak: int
    total_completions: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class HabitEntryBase(BaseModel):
    """Base schema for habit entry."""

    entry_date: date
    completed: bool = False
    notes: Optional[str] = None
    mood: Optional[str] = Field(None, max_length=20)


class HabitEntryCreate(HabitEntryBase):
    """Schema for creating habit entry."""

    pass


class HabitEntryUpdate(BaseModel):
    """Schema for updating habit entry."""

    completed: Optional[bool] = None
    notes: Optional[str] = None
    mood: Optional[str] = Field(None, max_length=20)


class HabitEntryResponse(HabitEntryBase):
    """Schema for habit entry response."""

    id: UUID
    habit_id: UUID
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
