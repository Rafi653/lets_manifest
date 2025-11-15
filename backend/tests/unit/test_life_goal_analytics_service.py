"""
Unit tests for life goal analytics service.
"""

from datetime import datetime, timedelta
from decimal import Decimal

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.goal import Goal, GoalMilestone
from app.models.user import User
from app.services.life_goal_analytics_service import LifeGoalAnalyticsService


@pytest.mark.asyncio
async def test_get_life_goals_summary_empty(db_session: AsyncSession):
    """Test getting summary when user has no life goals."""
    user = User(
        email="empty@example.com",
        username="emptyuser",
        password_hash="hashedpassword",
    )
    db_session.add(user)
    await db_session.flush()

    service = LifeGoalAnalyticsService(db_session)
    summary = await service.get_life_goals_summary(user.id)

    assert summary["total_goals"] == 0
    assert summary["active_goals"] == 0
    assert summary["completed_goals"] == 0
    assert summary["completion_rate"] == 0


@pytest.mark.asyncio
async def test_get_life_goals_summary_with_goals(db_session: AsyncSession):
    """Test getting summary with multiple life goals."""
    user = User(
        email="summary@example.com",
        username="summaryuser",
        password_hash="hashedpassword",
    )
    db_session.add(user)
    await db_session.flush()

    # Create life goals
    goals = [
        Goal(
            user_id=user.id,
            title="Investment Goal",
            goal_type="life_goal",
            category="investment",
            status="active",
        ),
        Goal(
            user_id=user.id,
            title="Travel Goal",
            goal_type="life_goal",
            category="travel",
            status="completed",
            completed_at=datetime.utcnow(),
        ),
        Goal(
            user_id=user.id,
            title="Health Goal",
            goal_type="life_goal",
            category="health",
            status="in_progress",
        ),
        Goal(
            user_id=user.id,
            title="Career Goal",
            goal_type="life_goal",
            category="career",
            status="cancelled",
        ),
    ]
    db_session.add_all(goals)
    await db_session.flush()

    service = LifeGoalAnalyticsService(db_session)
    summary = await service.get_life_goals_summary(user.id)

    assert summary["total_goals"] == 4
    assert summary["active_goals"] == 2  # active + in_progress
    assert summary["completed_goals"] == 1
    assert summary["cancelled_goals"] == 1
    assert summary["completion_rate"] == 25.0  # 1/4 * 100
    assert "investment" in summary["goals_by_category"]
    assert summary["goals_by_category"]["investment"] == 1


@pytest.mark.asyncio
async def test_get_milestone_statistics_no_milestones(db_session: AsyncSession):
    """Test milestone statistics when there are no milestones."""
    user = User(
        email="nomilestones@example.com",
        username="nomilestonesuser",
        password_hash="hashedpassword",
    )
    db_session.add(user)
    await db_session.flush()

    goal = Goal(
        user_id=user.id,
        title="Goal Without Milestones",
        goal_type="life_goal",
        category="test",
    )
    db_session.add(goal)
    await db_session.flush()

    service = LifeGoalAnalyticsService(db_session)
    stats = await service.get_milestone_statistics(user.id, goal.id)

    assert stats["total_milestones"] == 0
    assert stats["completed_milestones"] == 0
    assert stats["completion_rate"] == 0


@pytest.mark.asyncio
async def test_get_milestone_statistics_with_milestones(db_session: AsyncSession):
    """Test milestone statistics with various milestone statuses."""
    user = User(
        email="milestats@example.com",
        username="milestatsuser",
        password_hash="hashedpassword",
    )
    db_session.add(user)
    await db_session.flush()

    goal = Goal(
        user_id=user.id,
        title="Goal With Milestones",
        goal_type="life_goal",
        category="test",
    )
    db_session.add(goal)
    await db_session.flush()

    # Create milestones with different statuses
    milestones = [
        GoalMilestone(
            goal_id=goal.id,
            title="Completed Milestone 1",
            status="completed",
            order_index=1,
        ),
        GoalMilestone(
            goal_id=goal.id,
            title="Completed Milestone 2",
            status="completed",
            order_index=2,
        ),
        GoalMilestone(
            goal_id=goal.id,
            title="In Progress Milestone",
            status="in_progress",
            order_index=3,
        ),
        GoalMilestone(
            goal_id=goal.id,
            title="Pending Milestone",
            status="pending",
            order_index=4,
        ),
        GoalMilestone(
            goal_id=goal.id,
            title="Skipped Milestone",
            status="skipped",
            order_index=5,
        ),
    ]
    db_session.add_all(milestones)
    await db_session.flush()

    service = LifeGoalAnalyticsService(db_session)
    stats = await service.get_milestone_statistics(user.id, goal.id)

    assert stats["total_milestones"] == 5
    assert stats["completed_milestones"] == 2
    assert stats["in_progress_milestones"] == 1
    assert stats["pending_milestones"] == 1
    assert stats["skipped_milestones"] == 1
    assert stats["completion_rate"] == 40.0  # 2/5 * 100


@pytest.mark.asyncio
async def test_get_goals_by_life_area(db_session: AsyncSession):
    """Test grouping goals by life area."""
    user = User(
        email="byarea@example.com",
        username="byareauser",
        password_hash="hashedpassword",
    )
    db_session.add(user)
    await db_session.flush()

    # Create life goals in different areas
    goals = [
        Goal(
            user_id=user.id,
            title="Investment Goal 1",
            goal_type="life_goal",
            category="investment",
            status="active",
        ),
        Goal(
            user_id=user.id,
            title="Investment Goal 2",
            goal_type="life_goal",
            category="investment",
            status="completed",
        ),
        Goal(
            user_id=user.id,
            title="Travel Goal",
            goal_type="life_goal",
            category="travel",
            status="active",
        ),
        Goal(
            user_id=user.id,
            title="Health Goal",
            goal_type="life_goal",
            category="health",
            status="in_progress",
        ),
    ]
    db_session.add_all(goals)
    await db_session.flush()

    service = LifeGoalAnalyticsService(db_session)
    goals_by_area = await service.get_goals_by_life_area(user.id)

    # Should have 3 life areas
    assert len(goals_by_area) == 3
    
    # Find investment area
    investment_area = next(area for area in goals_by_area if area["life_area"] == "investment")
    assert investment_area["goal_count"] == 2
    
    # Find travel area
    travel_area = next(area for area in goals_by_area if area["life_area"] == "travel")
    assert travel_area["goal_count"] == 1
    
    # Find health area
    health_area = next(area for area in goals_by_area if area["life_area"] == "health")
    assert health_area["goal_count"] == 1


@pytest.mark.asyncio
async def test_get_milestone_statistics_all_goals(db_session: AsyncSession):
    """Test milestone statistics across all user's life goals."""
    user = User(
        email="allgoals@example.com",
        username="allgoalsuser",
        password_hash="hashedpassword",
    )
    db_session.add(user)
    await db_session.flush()

    # Create multiple life goals with milestones
    goal1 = Goal(
        user_id=user.id,
        title="Goal 1",
        goal_type="life_goal",
        category="test1",
    )
    goal2 = Goal(
        user_id=user.id,
        title="Goal 2",
        goal_type="life_goal",
        category="test2",
    )
    db_session.add_all([goal1, goal2])
    await db_session.flush()

    # Add milestones to both goals
    milestones = [
        GoalMilestone(goal_id=goal1.id, title="M1", status="completed", order_index=1),
        GoalMilestone(goal_id=goal1.id, title="M2", status="pending", order_index=2),
        GoalMilestone(goal_id=goal2.id, title="M3", status="completed", order_index=1),
        GoalMilestone(goal_id=goal2.id, title="M4", status="in_progress", order_index=2),
    ]
    db_session.add_all(milestones)
    await db_session.flush()

    service = LifeGoalAnalyticsService(db_session)
    # Get stats without specifying goal_id (all goals)
    stats = await service.get_milestone_statistics(user.id, goal_id=None)

    assert stats["total_milestones"] == 4
    assert stats["completed_milestones"] == 2
    assert stats["in_progress_milestones"] == 1
    assert stats["pending_milestones"] == 1
    assert stats["completion_rate"] == 50.0  # 2/4 * 100


@pytest.mark.asyncio
async def test_completion_time_calculation(db_session: AsyncSession):
    """Test average time to completion calculation."""
    user = User(
        email="timecalc@example.com",
        username="timecalcuser",
        password_hash="hashedpassword",
    )
    db_session.add(user)
    await db_session.flush()

    # Create completed goals with known time spans
    base_time = datetime.utcnow()
    
    goal1 = Goal(
        user_id=user.id,
        title="Quick Goal",
        goal_type="life_goal",
        category="test",
        status="completed",
        created_at=base_time - timedelta(days=30),
        completed_at=base_time,
    )
    
    goal2 = Goal(
        user_id=user.id,
        title="Longer Goal",
        goal_type="life_goal",
        category="test",
        status="completed",
        created_at=base_time - timedelta(days=90),
        completed_at=base_time,
    )
    
    db_session.add_all([goal1, goal2])
    await db_session.flush()

    service = LifeGoalAnalyticsService(db_session)
    summary = await service.get_life_goals_summary(user.id)

    # Average should be (30 + 90) / 2 = 60 days
    assert summary["avg_days_to_complete"] == 60.0
