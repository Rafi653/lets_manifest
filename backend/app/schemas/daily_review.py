"""
Daily review-related Pydantic schemas.
"""
from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class DailyReviewBase(BaseModel):
    """Base schema for daily review."""
    review_date: date
    mood_rating: Optional[int] = Field(None, ge=1, le=10)
    energy_level: Optional[int] = Field(None, ge=1, le=10)
    productivity_rating: Optional[int] = Field(None, ge=1, le=10)
    sleep_hours: Optional[Decimal] = Field(None, ge=0, le=24)
    sleep_quality: Optional[int] = Field(None, ge=1, le=10)
    water_intake_ml: Optional[int] = Field(None, ge=0)
    accomplishments: Optional[str] = None
    challenges: Optional[str] = None
    lessons_learned: Optional[str] = None
    gratitude: Optional[str] = None
    tomorrow_intentions: Optional[str] = None
    highlights: Optional[str] = None


class DailyReviewCreate(DailyReviewBase):
    """Schema for creating daily review."""
    pass


class DailyReviewUpdate(BaseModel):
    """Schema for updating daily review."""
    mood_rating: Optional[int] = Field(None, ge=1, le=10)
    energy_level: Optional[int] = Field(None, ge=1, le=10)
    productivity_rating: Optional[int] = Field(None, ge=1, le=10)
    sleep_hours: Optional[Decimal] = Field(None, ge=0, le=24)
    sleep_quality: Optional[int] = Field(None, ge=1, le=10)
    water_intake_ml: Optional[int] = Field(None, ge=0)
    accomplishments: Optional[str] = None
    challenges: Optional[str] = None
    lessons_learned: Optional[str] = None
    gratitude: Optional[str] = None
    tomorrow_intentions: Optional[str] = None
    highlights: Optional[str] = None


class DailyReviewResponse(DailyReviewBase):
    """Schema for daily review response."""
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
