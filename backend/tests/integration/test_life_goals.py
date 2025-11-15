"""
Integration tests for life goals functionality with milestones.
"""

from datetime import date, timedelta
from decimal import Decimal

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.goal import Goal, GoalMilestone
from app.models.user import User


@pytest.mark.asyncio
async def test_create_life_goal(db_session: AsyncSession):
    """Test creating a life goal without specific dates."""
    # Create a user first
    user = User(
        email="lifegoaluser@example.com",
        username="lifegoaluser",
        password_hash="hashedpassword",
    )
    db_session.add(user)
    await db_session.flush()

    # Create a life goal
    goal = Goal(
        user_id=user.id,
        title="Complete Real Estate Investment",
        description="Purchase first investment property",
        goal_type="life_goal",
        category="investment",
        status="active",
        priority=5,
    )
    db_session.add(goal)
    await db_session.flush()

    assert goal.id is not None
    assert goal.title == "Complete Real Estate Investment"
    assert goal.goal_type == "life_goal"
    assert goal.category == "investment"
    assert goal.start_date is None
    assert goal.end_date is None


@pytest.mark.asyncio
async def test_life_goal_with_milestones(db_session: AsyncSession):
    """Test creating a life goal with multiple milestones."""
    from sqlalchemy.orm import selectinload

    # Create user and life goal
    user = User(
        email="milestone@example.com",
        username="milestoneuser",
        password_hash="hashedpassword",
    )
    db_session.add(user)
    await db_session.flush()

    goal = Goal(
        user_id=user.id,
        title="Travel to Japan",
        goal_type="life_goal",
        category="travel",
        status="in_progress",
    )
    db_session.add(goal)
    await db_session.flush()

    # Add milestones
    milestone1 = GoalMilestone(
        goal_id=goal.id,
        title="Save $5000 for trip",
        order_index=1,
        status="completed",
    )
    milestone2 = GoalMilestone(
        goal_id=goal.id,
        title="Book flights and accommodation",
        order_index=2,
        status="in_progress",
        target_date=date.today() + timedelta(days=30),
    )
    milestone3 = GoalMilestone(
        goal_id=goal.id,
        title="Get travel visa",
        order_index=3,
        status="pending",
        target_date=date.today() + timedelta(days=60),
    )
    db_session.add_all([milestone1, milestone2, milestone3])
    await db_session.flush()

    # Re-query with eager loading to verify relationship
    result = await db_session.execute(
        select(Goal).where(Goal.id == goal.id).options(selectinload(Goal.milestones))
    )
    reloaded_goal = result.scalar_one()
    assert len(reloaded_goal.milestones) == 3
    
    # Check milestone ordering
    milestones_sorted = sorted(reloaded_goal.milestones, key=lambda m: m.order_index)
    assert milestones_sorted[0].title == "Save $5000 for trip"
    assert milestones_sorted[0].status == "completed"
    assert milestones_sorted[1].title == "Book flights and accommodation"
    assert milestones_sorted[1].status == "in_progress"
    assert milestones_sorted[2].title == "Get travel visa"
    assert milestones_sorted[2].status == "pending"


@pytest.mark.asyncio
async def test_life_goal_type_constraint(db_session: AsyncSession):
    """Test that life_goal type is accepted in constraint."""
    user = User(
        email="constraint@example.com",
        username="constraintuser",
        password_hash="hashedpassword",
    )
    db_session.add(user)
    await db_session.flush()

    # Create goal with life_goal type - should succeed
    goal = Goal(
        user_id=user.id,
        title="Health Improvement Plan",
        goal_type="life_goal",
        category="health",
    )
    db_session.add(goal)
    await db_session.flush()
    
    assert goal.id is not None
    assert goal.goal_type == "life_goal"


@pytest.mark.asyncio
async def test_life_goal_in_progress_status(db_session: AsyncSession):
    """Test that in_progress status is accepted in constraint."""
    user = User(
        email="status@example.com",
        username="statususer",
        password_hash="hashedpassword",
    )
    db_session.add(user)
    await db_session.flush()

    goal = Goal(
        user_id=user.id,
        title="Career Transition",
        goal_type="life_goal",
        category="career",
        status="in_progress",
    )
    db_session.add(goal)
    await db_session.flush()

    assert goal.id is not None
    assert goal.status == "in_progress"


@pytest.mark.asyncio
async def test_multiple_life_goals_by_category(db_session: AsyncSession):
    """Test creating multiple life goals in different categories."""
    from sqlalchemy.orm import selectinload

    user = User(
        email="multiarea@example.com",
        username="multiareauser",
        password_hash="hashedpassword",
    )
    db_session.add(user)
    await db_session.flush()

    # Create life goals in different life areas
    goals = [
        Goal(
            user_id=user.id,
            title="Buy Investment Property",
            goal_type="life_goal",
            category="investment",
            priority=5,
        ),
        Goal(
            user_id=user.id,
            title="Visit 10 Countries",
            goal_type="life_goal",
            category="travel",
            priority=4,
        ),
        Goal(
            user_id=user.id,
            title="Complete Master's Degree",
            goal_type="life_goal",
            category="education",
            priority=5,
        ),
        Goal(
            user_id=user.id,
            title="Run a Marathon",
            goal_type="life_goal",
            category="health",
            priority=3,
        ),
    ]
    db_session.add_all(goals)
    await db_session.flush()

    # Verify all goals were created
    result = await db_session.execute(
        select(User).where(User.id == user.id).options(selectinload(User.goals))
    )
    reloaded_user = result.scalar_one()
    life_goals = [g for g in reloaded_user.goals if g.goal_type == "life_goal"]
    
    assert len(life_goals) == 4
    categories = [g.category for g in life_goals]
    assert "investment" in categories
    assert "travel" in categories
    assert "education" in categories
    assert "health" in categories


@pytest.mark.asyncio
async def test_milestone_status_constraint(db_session: AsyncSession):
    """Test that milestone status constraint is enforced."""
    from sqlalchemy.exc import IntegrityError

    user = User(
        email="milestone_status@example.com",
        username="milestonestatususer",
        password_hash="hashedpassword",
    )
    db_session.add(user)
    await db_session.flush()

    goal = Goal(
        user_id=user.id,
        title="Test Goal",
        goal_type="life_goal",
        category="test",
    )
    db_session.add(goal)
    await db_session.flush()

    # Try to create milestone with invalid status
    milestone = GoalMilestone(
        goal_id=goal.id,
        title="Invalid Milestone",
        status="invalid_status",  # Not in ('pending', 'in_progress', 'completed', 'skipped')
    )
    db_session.add(milestone)

    with pytest.raises(IntegrityError):
        await db_session.flush()


@pytest.mark.asyncio
async def test_delete_goal_cascades_to_milestones(db_session: AsyncSession):
    """Test that deleting a goal cascades to its milestones."""
    user = User(
        email="cascade@example.com",
        username="cascadeuser",
        password_hash="hashedpassword",
    )
    db_session.add(user)
    await db_session.flush()

    goal = Goal(
        user_id=user.id,
        title="Cascade Test Goal",
        goal_type="life_goal",
        category="test",
    )
    db_session.add(goal)
    await db_session.flush()

    milestone = GoalMilestone(
        goal_id=goal.id,
        title="Test Milestone",
        order_index=1,
    )
    db_session.add(milestone)
    await db_session.flush()
    milestone_id = milestone.id

    # Delete goal
    await db_session.delete(goal)
    await db_session.flush()

    # Verify milestone is also deleted
    result = await db_session.execute(
        select(GoalMilestone).where(GoalMilestone.id == milestone_id)
    )
    deleted_milestone = result.scalar_one_or_none()
    assert deleted_milestone is None


@pytest.mark.asyncio
async def test_mixed_goal_types(db_session: AsyncSession):
    """Test that regular goals and life goals can coexist for a user."""
    user = User(
        email="mixed@example.com",
        username="mixeduser",
        password_hash="hashedpassword",
    )
    db_session.add(user)
    await db_session.flush()

    # Create a regular daily goal
    daily_goal = Goal(
        user_id=user.id,
        title="Daily Exercise",
        goal_type="daily",
        start_date=date.today(),
        end_date=date.today(),
    )
    
    # Create a life goal
    life_goal = Goal(
        user_id=user.id,
        title="Career Change",
        goal_type="life_goal",
        category="career",
    )
    
    db_session.add_all([daily_goal, life_goal])
    await db_session.flush()

    # Query goals
    result = await db_session.execute(
        select(Goal).where(Goal.user_id == user.id)
    )
    goals = list(result.scalars().all())
    
    assert len(goals) == 2
    goal_types = [g.goal_type for g in goals]
    assert "daily" in goal_types
    assert "life_goal" in goal_types
