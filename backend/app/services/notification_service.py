"""
Notification service for business logic.
"""

from datetime import datetime, timedelta
from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.goal import Goal
from app.models.notification import Notification, NotificationSettings
from app.repositories.notification_repository import (
    NotificationRepository,
    NotificationSettingsRepository,
)
from app.schemas.notification import (
    NotificationCreate,
    NotificationSettingsCreate,
    NotificationSettingsUpdate,
    NotificationUpdate,
)


class NotificationService:
    """Service for notification-related operations."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = NotificationRepository(db)
        self.settings_repository = NotificationSettingsRepository(db)

    async def create_notification(
        self, user_id: UUID, notification_data: NotificationCreate
    ) -> Notification:
        """Create a new notification."""
        notification = Notification(user_id=user_id, **notification_data.model_dump())
        return await self.repository.create(notification)

    async def get_notification(
        self, notification_id: UUID, user_id: UUID
    ) -> Notification:
        """Get a notification by ID, ensuring it belongs to the user."""
        notification = await self.repository.get_by_id(notification_id)
        if not notification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found",
            )
        if notification.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this notification",
            )
        return notification

    async def get_user_notifications(
        self,
        user_id: UUID,
        is_read: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[List[Notification], int]:
        """Get all notifications for a user with pagination."""
        notifications = await self.repository.get_user_notifications(
            user_id, is_read, skip, limit
        )
        total = await self.repository.count_user_notifications(user_id, is_read)
        return notifications, total

    async def update_notification(
        self, notification_id: UUID, user_id: UUID, notification_data: NotificationUpdate
    ) -> Notification:
        """Update a notification."""
        notification = await self.get_notification(notification_id, user_id)
        update_data = notification_data.model_dump(exclude_unset=True)
        return await self.repository.update(notification, update_data)

    async def mark_as_read(
        self, notification_id: UUID, user_id: UUID
    ) -> Notification:
        """Mark a notification as read."""
        notification = await self.get_notification(notification_id, user_id)
        result = await self.repository.mark_as_read(notification_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found",
            )
        return result

    async def delete_notification(self, notification_id: UUID, user_id: UUID) -> bool:
        """Delete a notification."""
        notification = await self.get_notification(notification_id, user_id)
        return await self.repository.delete(notification.id)

    async def create_goal_reminder(
        self, goal: Goal, user_id: UUID
    ) -> Optional[Notification]:
        """Create a reminder notification for a goal based on its reminder settings."""
        if not goal.reminder_enabled or not goal.reminder_time:
            return None

        # Calculate scheduled time based on goal end_date and reminder settings
        scheduled_date = goal.end_date
        if goal.reminder_days_before and goal.reminder_days_before > 0:
            scheduled_date = goal.end_date - timedelta(days=goal.reminder_days_before)

        # Combine date with reminder time
        hour, minute = map(int, goal.reminder_time.split(":"))
        scheduled_datetime = datetime.combine(
            scheduled_date, datetime.min.time()
        ).replace(hour=hour, minute=minute)

        # Don't create reminder if scheduled time is in the past
        if scheduled_datetime <= datetime.utcnow():
            return None

        notification_data = NotificationCreate(
            title=f"Reminder: {goal.title}",
            message=f"Your goal '{goal.title}' is coming up on {goal.end_date}",
            notification_type="reminder",
            scheduled_time=scheduled_datetime,
            goal_id=goal.id,
        )

        return await self.create_notification(user_id, notification_data)

    async def get_pending_notifications(
        self, before_time: datetime, limit: int = 100
    ) -> List[Notification]:
        """Get pending notifications scheduled before a certain time."""
        return await self.repository.get_pending_notifications(before_time, limit)

    async def process_pending_notifications(self) -> int:
        """Process pending notifications (to be called by a scheduler/worker)."""
        now = datetime.utcnow()
        notifications = await self.get_pending_notifications(now)

        processed_count = 0
        for notification in notifications:
            # Mark as sent (actual sending logic would be implemented here)
            await self.repository.mark_as_sent(notification.id)
            processed_count += 1

        return processed_count

    # Notification Settings methods

    async def get_user_settings(self, user_id: UUID) -> NotificationSettings:
        """Get notification settings for a user."""
        settings = await self.settings_repository.get_by_user_id(user_id)
        if not settings:
            # Create default settings if they don't exist
            settings = await self.settings_repository.create_default_settings(user_id)
        return settings

    async def create_settings(
        self, user_id: UUID, settings_data: NotificationSettingsCreate
    ) -> NotificationSettings:
        """Create notification settings for a user."""
        # Check if settings already exist
        existing = await self.settings_repository.get_by_user_id(user_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Notification settings already exist for this user",
            )

        settings = NotificationSettings(
            user_id=user_id, **settings_data.model_dump()
        )
        return await self.settings_repository.create(settings)

    async def update_settings(
        self, user_id: UUID, settings_data: NotificationSettingsUpdate
    ) -> NotificationSettings:
        """Update notification settings for a user."""
        settings = await self.get_user_settings(user_id)
        update_data = settings_data.model_dump(exclude_unset=True)
        return await self.settings_repository.update(settings, update_data)
