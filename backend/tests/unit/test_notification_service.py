"""
Unit tests for the notification service.
"""

from datetime import datetime, timedelta, date
from decimal import Decimal

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.goal import Goal
from app.models.user import User
from app.schemas.notification import (
    NotificationCreate,
    NotificationSettingsCreate,
    NotificationSettingsUpdate,
)
from app.services.notification_service import NotificationService


@pytest.mark.asyncio
async def test_create_notification_service(db_session: AsyncSession):
    """Test creating a notification via service."""
    # Create a user
    user = User(
        email="service@example.com",
        username="serviceuser",
        password_hash="hashedpassword",
    )
    db_session.add(user)
    await db_session.flush()

    # Create notification via service
    service = NotificationService(db_session)
    notification_data = NotificationCreate(
        title="Test Notification",
        message="Test message",
        notification_type="reminder",
        scheduled_time=datetime.utcnow() + timedelta(hours=1),
    )

    notification = await service.create_notification(user.id, notification_data)

    assert notification.id is not None
    assert notification.user_id == user.id
    assert notification.title == "Test Notification"


@pytest.mark.asyncio
async def test_get_user_notifications(db_session: AsyncSession):
    """Test getting notifications for a user."""
    # Create a user
    user = User(
        email="getnotif@example.com",
        username="getnotifuser",
        password_hash="hashedpassword",
    )
    db_session.add(user)
    await db_session.flush()

    # Create notifications
    service = NotificationService(db_session)
    for i in range(5):
        notification_data = NotificationCreate(
            title=f"Notification {i}",
            notification_type="reminder",
            scheduled_time=datetime.utcnow() + timedelta(hours=i),
        )
        await service.create_notification(user.id, notification_data)

    # Get notifications
    notifications, total = await service.get_user_notifications(user.id)

    assert total == 5
    assert len(notifications) == 5


@pytest.mark.asyncio
async def test_mark_notification_as_read(db_session: AsyncSession):
    """Test marking a notification as read."""
    # Create a user
    user = User(
        email="markread@example.com",
        username="markreaduser",
        password_hash="hashedpassword",
    )
    db_session.add(user)
    await db_session.flush()

    # Create notification
    service = NotificationService(db_session)
    notification_data = NotificationCreate(
        title="Unread Notification",
        notification_type="reminder",
        scheduled_time=datetime.utcnow(),
    )
    notification = await service.create_notification(user.id, notification_data)

    assert notification.is_read is False

    # Mark as read
    updated = await service.mark_as_read(notification.id, user.id)

    assert updated.is_read is True


@pytest.mark.asyncio
async def test_create_goal_reminder(db_session: AsyncSession):
    """Test creating a reminder for a goal."""
    # Create a user
    user = User(
        email="goalremind@example.com",
        username="goalreminduser",
        password_hash="hashedpassword",
    )
    db_session.add(user)
    await db_session.flush()

    # Create goal with reminder settings
    goal = Goal(
        user_id=user.id,
        title="Test Goal",
        goal_type="weekly",
        start_date=date.today(),
        end_date=date.today() + timedelta(days=7),
        reminder_enabled=True,
        reminder_time="10:00",
        reminder_days_before=1,
    )
    db_session.add(goal)
    await db_session.flush()

    # Create reminder via service
    service = NotificationService(db_session)
    notification = await service.create_goal_reminder(goal, user.id)

    assert notification is not None
    assert notification.goal_id == goal.id
    assert notification.notification_type == "reminder"
    assert "Test Goal" in notification.title


@pytest.mark.asyncio
async def test_create_goal_reminder_disabled(db_session: AsyncSession):
    """Test that reminder is not created if disabled on goal."""
    # Create a user
    user = User(
        email="noremind@example.com",
        username="noreminduser",
        password_hash="hashedpassword",
    )
    db_session.add(user)
    await db_session.flush()

    # Create goal with reminder disabled
    goal = Goal(
        user_id=user.id,
        title="No Reminder Goal",
        goal_type="daily",
        start_date=date.today(),
        end_date=date.today() + timedelta(days=1),
        reminder_enabled=False,
    )
    db_session.add(goal)
    await db_session.flush()

    # Try to create reminder
    service = NotificationService(db_session)
    notification = await service.create_goal_reminder(goal, user.id)

    assert notification is None


@pytest.mark.asyncio
async def test_get_pending_notifications(db_session: AsyncSession):
    """Test getting pending notifications."""
    # Create a user
    user = User(
        email="pending@example.com",
        username="pendinguser",
        password_hash="hashedpassword",
    )
    db_session.add(user)
    await db_session.flush()

    # Create notifications with different statuses and times
    service = NotificationService(db_session)

    # Past pending notification
    past_notif = NotificationCreate(
        title="Past Notification",
        notification_type="reminder",
        scheduled_time=datetime.utcnow() - timedelta(hours=1),
    )
    await service.create_notification(user.id, past_notif)

    # Future pending notification
    future_notif = NotificationCreate(
        title="Future Notification",
        notification_type="reminder",
        scheduled_time=datetime.utcnow() + timedelta(hours=1),
    )
    await service.create_notification(user.id, future_notif)

    # Get pending notifications before now
    pending = await service.get_pending_notifications(datetime.utcnow())

    assert len(pending) == 1
    assert pending[0].title == "Past Notification"


@pytest.mark.asyncio
async def test_notification_settings_crud(db_session: AsyncSession):
    """Test CRUD operations on notification settings."""
    # Create a user
    user = User(
        email="settingscrud@example.com",
        username="settingscruduser",
        password_hash="hashedpassword",
    )
    db_session.add(user)
    await db_session.flush()

    service = NotificationService(db_session)

    # Get or create default settings
    settings = await service.get_user_settings(user.id)
    assert settings is not None
    assert settings.user_id == user.id

    # Update settings
    update_data = NotificationSettingsUpdate(
        email_enabled=False,
        browser_enabled=True,
        default_reminder_time="08:00",
    )
    updated = await service.update_settings(user.id, update_data)

    assert updated.email_enabled is False
    assert updated.browser_enabled is True
    assert updated.default_reminder_time == "08:00"


@pytest.mark.asyncio
async def test_filter_notifications_by_read_status(db_session: AsyncSession):
    """Test filtering notifications by read status."""
    # Create a user
    user = User(
        email="filter@example.com",
        username="filteruser",
        password_hash="hashedpassword",
    )
    db_session.add(user)
    await db_session.flush()

    # Create notifications
    service = NotificationService(db_session)

    # Create 3 unread notifications
    for i in range(3):
        notification_data = NotificationCreate(
            title=f"Unread {i}",
            notification_type="reminder",
            scheduled_time=datetime.utcnow(),
        )
        await service.create_notification(user.id, notification_data)

    # Create 2 read notifications
    for i in range(2):
        notification_data = NotificationCreate(
            title=f"Read {i}",
            notification_type="reminder",
            scheduled_time=datetime.utcnow(),
        )
        notif = await service.create_notification(user.id, notification_data)
        await service.mark_as_read(notif.id, user.id)

    # Get unread notifications
    unread, unread_total = await service.get_user_notifications(
        user.id, is_read=False
    )
    assert unread_total == 3

    # Get read notifications
    read, read_total = await service.get_user_notifications(user.id, is_read=True)
    assert read_total == 2

    # Get all notifications
    all_notifs, all_total = await service.get_user_notifications(user.id)
    assert all_total == 5
