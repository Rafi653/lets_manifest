"""
Goal-related Pydantic schemas.
"""
from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class GoalBase(BaseModel):
    """Base schema for goal."""
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    goal_type: str = Field(..., pattern="^(daily|weekly|monthly|yearly)$")
    category: Optional[str] = Field(None, max_length=50)
    target_value: Optional[Decimal] = None
    target_unit: Optional[str] = Field(None, max_length=50)
    start_date: date
    end_date: date
    priority: int = Field(default=0, ge=0, le=5)
    is_recurring: bool = False
    recurrence_pattern: Optional[str] = Field(None, max_length=50)
    parent_goal_id: Optional[UUID] = None


class GoalCreate(GoalBase):
    """Schema for creating a goal."""
    pass


class GoalUpdate(BaseModel):
    """Schema for updating a goal."""
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = Field(None, max_length=50)
    target_value: Optional[Decimal] = None
    target_unit: Optional[str] = Field(None, max_length=50)
    end_date: Optional[date] = None
    status: Optional[str] = Field(None, pattern="^(active|completed|cancelled|paused)$")
    priority: Optional[int] = Field(None, ge=0, le=5)
    current_value: Optional[Decimal] = None


class GoalResponse(GoalBase):
    """Schema for goal response."""
    id: UUID
    user_id: UUID
    current_value: Decimal
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class GoalProgressBase(BaseModel):
    """Base schema for goal progress."""
    progress_date: date
    value: Decimal
    notes: Optional[str] = None


class GoalProgressCreate(GoalProgressBase):
    """Schema for creating goal progress."""
    pass


class GoalProgressResponse(GoalProgressBase):
    """Schema for goal progress response."""
    id: UUID
    goal_id: UUID
    percentage: Optional[Decimal] = None
    created_at: datetime

    class Config:
        from_attributes = True
