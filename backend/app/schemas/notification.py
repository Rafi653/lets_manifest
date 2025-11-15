"""
Notification-related Pydantic schemas.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class NotificationBase(BaseModel):
    """Base schema for notification."""

    title: str = Field(..., max_length=255)
    message: Optional[str] = None
    notification_type: str = Field(
        ..., pattern="^(reminder|goal_deadline|goal_completed|system)$"
    )
    scheduled_time: datetime


class NotificationCreate(NotificationBase):
    """Schema for creating a notification."""

    goal_id: Optional[UUID] = None


class NotificationUpdate(BaseModel):
    """Schema for updating a notification."""

    is_read: Optional[bool] = None
    status: Optional[str] = Field(
        None, pattern="^(pending|sent|failed|cancelled)$"
    )


class NotificationResponse(NotificationBase):
    """Schema for notification response."""

    id: UUID
    user_id: UUID
    goal_id: Optional[UUID] = None
    sent_at: Optional[datetime] = None
    status: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationSettingsBase(BaseModel):
    """Base schema for notification settings."""

    email_enabled: bool = True
    email_reminders: bool = True
    email_goal_updates: bool = True
    browser_enabled: bool = False
    browser_reminders: bool = False
    default_reminder_time: str = Field("09:00", pattern="^([0-1][0-9]|2[0-3]):[0-5][0-9]$")
    reminder_before_hours: str = "24"


class NotificationSettingsCreate(NotificationSettingsBase):
    """Schema for creating notification settings."""

    pass


class NotificationSettingsUpdate(BaseModel):
    """Schema for updating notification settings."""

    email_enabled: Optional[bool] = None
    email_reminders: Optional[bool] = None
    email_goal_updates: Optional[bool] = None
    browser_enabled: Optional[bool] = None
    browser_reminders: Optional[bool] = None
    default_reminder_time: Optional[str] = Field(
        None, pattern="^([0-1][0-9]|2[0-3]):[0-5][0-9]$"
    )
    reminder_before_hours: Optional[str] = None


class NotificationSettingsResponse(NotificationSettingsBase):
    """Schema for notification settings response."""

    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
