"""
Notification models for reminder and notification system.
"""

from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class Notification(Base):
    """Notification model for user notifications and reminders."""

    __tablename__ = "notifications"

    # Foreign keys
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )
    goal_id = Column(UUID(as_uuid=True), ForeignKey("goals.id"), index=True)

    # Notification content
    title = Column(String(255), nullable=False)
    message = Column(Text)
    notification_type = Column(String(50), nullable=False, index=True)

    # Scheduling
    scheduled_time = Column(DateTime, nullable=False, index=True)
    sent_at = Column(DateTime)

    # Status
    status = Column(String(20), default="pending", nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)

    # Constraints
    __table_args__ = (
        CheckConstraint(
            "notification_type IN ('reminder', 'goal_deadline', 'goal_completed', 'system')",
            name="ck_notification_type",
        ),
        CheckConstraint(
            "status IN ('pending', 'sent', 'failed', 'cancelled')",
            name="ck_notification_status",
        ),
    )

    # Relationships
    user = relationship("User", back_populates="notifications")
    goal = relationship("Goal", back_populates="notifications")

    def __repr__(self) -> str:
        return f"<Notification(id={self.id}, type={self.notification_type}, status={self.status})>"


class NotificationSettings(Base):
    """User notification preferences and settings."""

    __tablename__ = "notification_settings"

    # Foreign key
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        unique=True,
        index=True,
    )

    # Email notifications
    email_enabled = Column(Boolean, default=True, nullable=False)
    email_reminders = Column(Boolean, default=True, nullable=False)
    email_goal_updates = Column(Boolean, default=True, nullable=False)

    # Browser notifications
    browser_enabled = Column(Boolean, default=False, nullable=False)
    browser_reminders = Column(Boolean, default=False, nullable=False)

    # Reminder preferences
    default_reminder_time = Column(String(5), default="09:00")  # HH:MM format
    reminder_before_hours = Column(
        String(50), default="24"
    )  # Hours before goal deadline

    # Timestamps
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="notification_settings")

    def __repr__(self) -> str:
        return f"<NotificationSettings(user_id={self.user_id})>"
