"""
Integration tests for CRUD operations on Goal and GoalProgress models.
"""

from datetime import date, timedelta
from decimal import Decimal

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.goal import Goal, GoalProgress
from app.models.user import User


@pytest.mark.asyncio
async def test_create_goal(db_session: AsyncSession):
    """Test creating a new goal."""
    # Create a user first
    user = User(
        email="goaluser@example.com",
        username="goaluser",
        password_hash="hashedpassword",
    )
    db_session.add(user)
    await db_session.flush()

    # Create a goal
    goal = Goal(
        user_id=user.id,
        title="Complete Marathon",
        description="Run a full marathon",
        goal_type="yearly",
        category="fitness",
        target_value=Decimal("42.195"),
        target_unit="km",
        current_value=Decimal("0"),
        start_date=date(2025, 1, 1),
        end_date=date(2025, 12, 31),
        status="active",
        priority=5,
    )
    db_session.add(goal)
    await db_session.flush()

    assert goal.id is not None
    assert goal.title == "Complete Marathon"
    assert goal.goal_type == "yearly"
    assert goal.current_value == Decimal("0")


@pytest.mark.asyncio
async def test_goal_with_progress(db_session: AsyncSession):
    """Test creating a goal with progress entries."""
    from sqlalchemy.orm import selectinload

    # Create user and goal
    user = User(
        email="progress@example.com",
        username="progressuser",
        password_hash="hashedpassword",
    )
    db_session.add(user)
    await db_session.flush()

    goal = Goal(
        user_id=user.id,
        title="Weight Loss Goal",
        goal_type="monthly",
        target_value=Decimal("5"),
        target_unit="kg",
        start_date=date.today(),
        end_date=date.today() + timedelta(days=30),
    )
    db_session.add(goal)
    await db_session.flush()

    # Add progress entries
    progress1 = GoalProgress(
        goal_id=goal.id,
        progress_date=date.today(),
        value=Decimal("1.5"),
        percentage=Decimal("30"),
        notes="Good progress this week",
    )
    progress2 = GoalProgress(
        goal_id=goal.id,
        progress_date=date.today() + timedelta(days=7),
        value=Decimal("3.0"),
        percentage=Decimal("60"),
        notes="Halfway there!",
    )
    db_session.add_all([progress1, progress2])
    await db_session.flush()

    # Re-query with eager loading to verify relationship
    result = await db_session.execute(
        select(Goal)
        .where(Goal.id == goal.id)
        .options(selectinload(Goal.progress_entries))
    )
    reloaded_goal = result.scalar_one()
    assert len(reloaded_goal.progress_entries) == 2
    assert reloaded_goal.progress_entries[0].value == Decimal("1.5")
    assert reloaded_goal.progress_entries[1].value == Decimal("3.0")


@pytest.mark.asyncio
async def test_user_goal_relationship(db_session: AsyncSession):
    """Test the relationship between User and Goals."""
    from sqlalchemy.orm import selectinload

    user = User(
        email="multigoal@example.com",
        username="multigoaluser",
        password_hash="hashedpassword",
    )
    db_session.add(user)
    await db_session.flush()

    # Create multiple goals for the user
    goal1 = Goal(
        user_id=user.id,
        title="Daily Meditation",
        goal_type="daily",
        start_date=date.today(),
        end_date=date.today(),
    )
    goal2 = Goal(
        user_id=user.id,
        title="Weekly Running",
        goal_type="weekly",
        start_date=date.today(),
        end_date=date.today() + timedelta(days=7),
    )
    db_session.add_all([goal1, goal2])
    await db_session.flush()

    # Re-query with eager loading to verify relationship
    result = await db_session.execute(
        select(User).where(User.id == user.id).options(selectinload(User.goals))
    )
    reloaded_user = result.scalar_one()
    assert len(reloaded_user.goals) == 2
    assert reloaded_user.goals[0].title in ["Daily Meditation", "Weekly Running"]


@pytest.mark.asyncio
async def test_goal_type_constraint(db_session: AsyncSession):
    """Test that goal_type constraint is enforced."""
    from sqlalchemy.exc import IntegrityError

    user = User(
        email="constraint@example.com",
        username="constraintuser",
        password_hash="hashedpassword",
    )
    db_session.add(user)
    await db_session.flush()

    # Try to create goal with invalid type
    goal = Goal(
        user_id=user.id,
        title="Invalid Goal",
        goal_type="invalid_type",  # Not in ('daily', 'weekly', 'monthly', 'yearly')
        start_date=date.today(),
        end_date=date.today(),
    )
    db_session.add(goal)

    with pytest.raises(IntegrityError):
        await db_session.flush()


@pytest.mark.asyncio
async def test_goal_status_constraint(db_session: AsyncSession):
    """Test that goal status constraint is enforced."""
    from sqlalchemy.exc import IntegrityError

    user = User(
        email="status@example.com",
        username="statususer",
        password_hash="hashedpassword",
    )
    db_session.add(user)
    await db_session.flush()

    goal = Goal(
        user_id=user.id,
        title="Status Test",
        goal_type="daily",
        start_date=date.today(),
        end_date=date.today(),
        status="invalid_status",  # Not in ('active', 'completed', 'cancelled', 'paused')
    )
    db_session.add(goal)

    with pytest.raises(IntegrityError):
        await db_session.flush()


@pytest.mark.asyncio
async def test_delete_user_cascades_to_goals(db_session: AsyncSession):
    """Test that deleting a user cascades to their goals."""
    user = User(
        email="cascade@example.com",
        username="cascadeuser",
        password_hash="hashedpassword",
    )
    db_session.add(user)
    await db_session.flush()

    goal = Goal(
        user_id=user.id,
        title="Cascade Test",
        goal_type="daily",
        start_date=date.today(),
        end_date=date.today(),
    )
    db_session.add(goal)
    await db_session.flush()
    goal_id = goal.id

    # Delete user
    await db_session.delete(user)
    await db_session.flush()

    # Verify goal is also deleted
    result = await db_session.execute(select(Goal).where(Goal.id == goal_id))
    deleted_goal = result.scalar_one_or_none()
    assert deleted_goal is None


@pytest.mark.asyncio
async def test_sub_goals(db_session: AsyncSession):
    """Test parent-child goal relationships."""
    user = User(
        email="subgoal@example.com",
        username="subgoaluser",
        password_hash="hashedpassword",
    )
    db_session.add(user)
    await db_session.flush()

    # Create parent goal
    parent_goal = Goal(
        user_id=user.id,
        title="Yearly Fitness Goal",
        goal_type="yearly",
        start_date=date(2025, 1, 1),
        end_date=date(2025, 12, 31),
    )
    db_session.add(parent_goal)
    await db_session.flush()

    # Create sub-goal
    sub_goal = Goal(
        user_id=user.id,
        parent_goal_id=parent_goal.id,
        title="Monthly Running Goal",
        goal_type="monthly",
        start_date=date.today(),
        end_date=date.today() + timedelta(days=30),
    )
    db_session.add(sub_goal)
    await db_session.flush()

    # Verify relationship
    assert sub_goal.parent_goal_id == parent_goal.id

    # Query sub-goals explicitly
    result = await db_session.execute(
        select(Goal).where(Goal.parent_goal_id == parent_goal.id)
    )
    sub_goals = result.scalars().all()
    assert len(sub_goals) == 1
    assert sub_goals[0].title == "Monthly Running Goal"
