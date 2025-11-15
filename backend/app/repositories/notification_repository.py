"""
Repository for notification-related database operations.
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.notification import Notification, NotificationSettings
from app.repositories.base_repository import BaseRepository


class NotificationRepository(BaseRepository[Notification]):
    """Repository for notification operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(db, Notification)

    async def get_user_notifications(
        self,
        user_id: UUID,
        is_read: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Notification]:
        """Get notifications for a user with optional filter."""
        query = select(Notification).where(Notification.user_id == user_id)

        if is_read is not None:
            query = query.where(Notification.is_read == is_read)

        query = query.order_by(Notification.scheduled_time.desc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_pending_notifications(
        self, before_time: datetime, limit: int = 100
    ) -> List[Notification]:
        """Get pending notifications scheduled before a certain time."""
        query = (
            select(Notification)
            .where(Notification.status == "pending")
            .where(Notification.scheduled_time <= before_time)
            .order_by(Notification.scheduled_time)
            .limit(limit)
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def mark_as_read(self, notification_id: UUID) -> Optional[Notification]:
        """Mark a notification as read."""
        notification = await self.get_by_id(notification_id)
        if notification:
            notification.is_read = True
            await self.db.flush()
            await self.db.refresh(notification)
        return notification

    async def mark_as_sent(self, notification_id: UUID) -> Optional[Notification]:
        """Mark a notification as sent."""
        notification = await self.get_by_id(notification_id)
        if notification:
            notification.status = "sent"
            notification.sent_at = datetime.utcnow()
            await self.db.flush()
            await self.db.refresh(notification)
        return notification

    async def count_user_notifications(
        self, user_id: UUID, is_read: Optional[bool] = None
    ) -> int:
        """Count notifications for a user."""
        query = select(Notification).where(Notification.user_id == user_id)

        if is_read is not None:
            query = query.where(Notification.is_read == is_read)

        result = await self.db.execute(query)
        return len(list(result.scalars().all()))


class NotificationSettingsRepository(BaseRepository[NotificationSettings]):
    """Repository for notification settings operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(db, NotificationSettings)

    async def get_by_user_id(self, user_id: UUID) -> Optional[NotificationSettings]:
        """Get notification settings for a user."""
        query = select(NotificationSettings).where(
            NotificationSettings.user_id == user_id
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create_default_settings(
        self, user_id: UUID
    ) -> NotificationSettings:
        """Create default notification settings for a new user."""
        settings = NotificationSettings(user_id=user_id)
        return await self.create(settings)
