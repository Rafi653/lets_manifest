"""
Integration tests for notification models and CRUD operations.
"""

from datetime import datetime, timedelta
from decimal import Decimal

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.goal import Goal
from app.models.notification import Notification, NotificationSettings
from app.models.user import User


@pytest.mark.asyncio
async def test_create_notification(db_session: AsyncSession):
    """Test creating a new notification."""
    # Create a user first
    user = User(
        email="notifuser@example.com",
        username="notifuser",
        password_hash="hashedpassword",
    )
    db_session.add(user)
    await db_session.flush()

    # Create a notification
    notification = Notification(
        user_id=user.id,
        title="Test Notification",
        message="This is a test notification",
        notification_type="reminder",
        scheduled_time=datetime.utcnow() + timedelta(hours=1),
        status="pending",
        is_read=False,
    )
    db_session.add(notification)
    await db_session.flush()

    assert notification.id is not None
    assert notification.title == "Test Notification"
    assert notification.notification_type == "reminder"
    assert notification.status == "pending"
    assert notification.is_read is False


@pytest.mark.asyncio
async def test_notification_with_goal(db_session: AsyncSession):
    """Test creating a notification linked to a goal."""
    from datetime import date

    # Create user
    user = User(
        email="goalnotif@example.com",
        username="goalnotifuser",
        password_hash="hashedpassword",
    )
    db_session.add(user)
    await db_session.flush()

    # Create goal
    goal = Goal(
        user_id=user.id,
        title="Complete Project",
        goal_type="weekly",
        start_date=date.today(),
        end_date=date.today() + timedelta(days=7),
        reminder_enabled=True,
        reminder_time="09:00",
        reminder_days_before=1,
    )
    db_session.add(goal)
    await db_session.flush()

    # Create notification for the goal
    notification = Notification(
        user_id=user.id,
        goal_id=goal.id,
        title=f"Reminder: {goal.title}",
        message="Your goal deadline is approaching",
        notification_type="reminder",
        scheduled_time=datetime.utcnow() + timedelta(days=1),
        status="pending",
        is_read=False,
    )
    db_session.add(notification)
    await db_session.flush()

    assert notification.goal_id == goal.id
    assert notification.title == "Reminder: Complete Project"


@pytest.mark.asyncio
async def test_user_notification_relationship(db_session: AsyncSession):
    """Test the relationship between User and Notifications."""
    from sqlalchemy.orm import selectinload

    user = User(
        email="multinotif@example.com",
        username="multinotifuser",
        password_hash="hashedpassword",
    )
    db_session.add(user)
    await db_session.flush()

    # Create multiple notifications for the user
    notif1 = Notification(
        user_id=user.id,
        title="Notification 1",
        notification_type="reminder",
        scheduled_time=datetime.utcnow(),
        status="pending",
        is_read=False,
    )
    notif2 = Notification(
        user_id=user.id,
        title="Notification 2",
        notification_type="system",
        scheduled_time=datetime.utcnow(),
        status="sent",
        is_read=True,
    )
    db_session.add_all([notif1, notif2])
    await db_session.flush()

    # Re-query with eager loading to verify relationship
    result = await db_session.execute(
        select(User).where(User.id == user.id).options(selectinload(User.notifications))
    )
    reloaded_user = result.scalar_one()
    assert len(reloaded_user.notifications) == 2


@pytest.mark.asyncio
async def test_notification_type_constraint(db_session: AsyncSession):
    """Test that notification_type constraint is enforced."""
    from sqlalchemy.exc import IntegrityError

    user = User(
        email="constraint@example.com",
        username="constraintuser",
        password_hash="hashedpassword",
    )
    db_session.add(user)
    await db_session.flush()

    # Try to create notification with invalid type
    notification = Notification(
        user_id=user.id,
        title="Invalid Notification",
        notification_type="invalid_type",
        scheduled_time=datetime.utcnow(),
        status="pending",
        is_read=False,
    )
    db_session.add(notification)

    with pytest.raises(IntegrityError):
        await db_session.flush()


@pytest.mark.asyncio
async def test_notification_status_constraint(db_session: AsyncSession):
    """Test that notification status constraint is enforced."""
    from sqlalchemy.exc import IntegrityError

    user = User(
        email="status@example.com",
        username="statususer",
        password_hash="hashedpassword",
    )
    db_session.add(user)
    await db_session.flush()

    notification = Notification(
        user_id=user.id,
        title="Status Test",
        notification_type="reminder",
        scheduled_time=datetime.utcnow(),
        status="invalid_status",
        is_read=False,
    )
    db_session.add(notification)

    with pytest.raises(IntegrityError):
        await db_session.flush()


@pytest.mark.asyncio
async def test_create_notification_settings(db_session: AsyncSession):
    """Test creating notification settings."""
    user = User(
        email="settings@example.com",
        username="settingsuser",
        password_hash="hashedpassword",
    )
    db_session.add(user)
    await db_session.flush()

    settings = NotificationSettings(
        user_id=user.id,
        email_enabled=True,
        email_reminders=True,
        email_goal_updates=False,
        browser_enabled=False,
        browser_reminders=False,
        default_reminder_time="09:00",
        reminder_before_hours="24",
    )
    db_session.add(settings)
    await db_session.flush()

    assert settings.id is not None
    assert settings.user_id == user.id
    assert settings.email_enabled is True
    assert settings.default_reminder_time == "09:00"


@pytest.mark.asyncio
async def test_user_notification_settings_relationship(db_session: AsyncSession):
    """Test the one-to-one relationship between User and NotificationSettings."""
    from sqlalchemy.orm import selectinload

    user = User(
        email="settingsrel@example.com",
        username="settingsreluser",
        password_hash="hashedpassword",
    )
    db_session.add(user)
    await db_session.flush()

    settings = NotificationSettings(user_id=user.id)
    db_session.add(settings)
    await db_session.flush()

    # Re-query with eager loading to verify relationship
    result = await db_session.execute(
        select(User)
        .where(User.id == user.id)
        .options(selectinload(User.notification_settings))
    )
    reloaded_user = result.scalar_one()
    assert reloaded_user.notification_settings is not None
    assert reloaded_user.notification_settings.user_id == user.id


@pytest.mark.asyncio
async def test_delete_user_cascades_to_notifications(db_session: AsyncSession):
    """Test that deleting a user cascades to their notifications."""
    user = User(
        email="cascade@example.com",
        username="cascadeuser",
        password_hash="hashedpassword",
    )
    db_session.add(user)
    await db_session.flush()

    notification = Notification(
        user_id=user.id,
        title="Cascade Test",
        notification_type="reminder",
        scheduled_time=datetime.utcnow(),
        status="pending",
        is_read=False,
    )
    db_session.add(notification)
    await db_session.flush()
    notification_id = notification.id

    # Delete user
    await db_session.delete(user)
    await db_session.flush()

    # Verify notification is also deleted
    result = await db_session.execute(
        select(Notification).where(Notification.id == notification_id)
    )
    deleted_notification = result.scalar_one_or_none()
    assert deleted_notification is None


@pytest.mark.asyncio
async def test_goal_with_reminder_settings(db_session: AsyncSession):
    """Test goal with reminder settings."""
    from datetime import date

    user = User(
        email="goalreminder@example.com",
        username="goalreminderuser",
        password_hash="hashedpassword",
    )
    db_session.add(user)
    await db_session.flush()

    goal = Goal(
        user_id=user.id,
        title="Goal with Reminder",
        goal_type="daily",
        start_date=date.today(),
        end_date=date.today() + timedelta(days=1),
        reminder_enabled=True,
        reminder_time="08:30",
        reminder_days_before=0,
    )
    db_session.add(goal)
    await db_session.flush()

    assert goal.reminder_enabled is True
    assert goal.reminder_time == "08:30"
    assert goal.reminder_days_before == 0
