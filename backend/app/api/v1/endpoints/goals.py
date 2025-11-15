"""
Goal endpoints.
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.common import APIResponse, PaginatedResponse
from app.schemas.goal import (
    GoalCreate,
    GoalUpdate,
    GoalResponse,
    GoalProgressCreate,
    GoalProgressResponse,
    GoalMilestoneCreate,
    GoalMilestoneUpdate,
    GoalMilestoneResponse,
)
from app.services.goal_service import GoalService
import math

router = APIRouter()


@router.post(
    "", response_model=APIResponse[GoalResponse], status_code=status.HTTP_201_CREATED
)
async def create_goal(
    goal_data: GoalCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new goal.

    - **title**: Goal title (required)
    - **description**: Optional description
    - **goal_type**: Type of goal (daily/weekly/monthly/yearly)
    - **target_value**: Target numeric value
    - **start_date**: Goal start date
    - **end_date**: Goal end date
    - **priority**: Priority level (0-5)
    """
    service = GoalService(db)
    goal = await service.create_goal(current_user.id, goal_data)

    return APIResponse(
        data=GoalResponse.model_validate(goal), message="Goal created successfully"
    )


@router.get("", response_model=APIResponse[PaginatedResponse[GoalResponse]])
async def list_goals(
    goal_type: Optional[str] = Query(None, description="Filter by goal type"),
    status_filter: Optional[str] = Query(None, description="Filter by status"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    List all goals for the current user with pagination and filtering.

    Query parameters:
    - **goal_type**: Filter by type (daily/weekly/monthly/yearly)
    - **status_filter**: Filter by status (active/completed/cancelled/paused)
    - **page**: Page number (default: 1)
    - **limit**: Items per page (default: 20, max: 100)
    """
    service = GoalService(db)
    skip = (page - 1) * limit
    goals, total = await service.get_user_goals(
        current_user.id, goal_type, status_filter, skip, limit
    )

    goal_responses = [GoalResponse.model_validate(goal) for goal in goals]

    return APIResponse(
        data=PaginatedResponse(
            items=goal_responses,
            total=total,
            page=page,
            limit=limit,
            total_pages=math.ceil(total / limit) if total > 0 else 0,
        ),
        message="Goals retrieved successfully",
    )


@router.get("/{goal_id}", response_model=APIResponse[GoalResponse])
async def get_goal(
    goal_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a specific goal by ID."""
    service = GoalService(db)
    goal = await service.get_goal(goal_id, current_user.id)

    return APIResponse(
        data=GoalResponse.model_validate(goal), message="Goal retrieved successfully"
    )


@router.put("/{goal_id}", response_model=APIResponse[GoalResponse])
async def update_goal(
    goal_id: UUID,
    goal_data: GoalUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Update a goal.

    All fields are optional. Only provided fields will be updated.
    """
    service = GoalService(db)
    goal = await service.update_goal(goal_id, current_user.id, goal_data)

    return APIResponse(
        data=GoalResponse.model_validate(goal), message="Goal updated successfully"
    )


@router.delete(
    "/{goal_id}", response_model=APIResponse[dict], status_code=status.HTTP_200_OK
)
async def delete_goal(
    goal_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a goal."""
    service = GoalService(db)
    deleted = await service.delete_goal(goal_id, current_user.id)

    return APIResponse(data={"deleted": deleted}, message="Goal deleted successfully")


@router.post(
    "/{goal_id}/progress",
    response_model=APIResponse[GoalProgressResponse],
    status_code=status.HTTP_201_CREATED,
)
async def add_goal_progress(
    goal_id: UUID,
    progress_data: GoalProgressCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Add progress to a goal.

    - **progress_date**: Date of progress entry
    - **value**: Progress value
    - **notes**: Optional notes
    """
    service = GoalService(db)
    progress = await service.add_progress(goal_id, current_user.id, progress_data)

    return APIResponse(
        data=GoalProgressResponse.model_validate(progress),
        message="Progress added successfully",
    )


@router.get(
    "/{goal_id}/progress", response_model=APIResponse[list[GoalProgressResponse]]
)
async def get_goal_progress(
    goal_id: UUID,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get progress entries for a goal."""
    service = GoalService(db)
    skip = (page - 1) * limit
    progress_entries = await service.get_goal_progress(
        goal_id, current_user.id, skip, limit
    )

    return APIResponse(
        data=[GoalProgressResponse.model_validate(p) for p in progress_entries],
        message="Progress entries retrieved successfully",
    )


@router.post(
    "/{goal_id}/milestones",
    response_model=APIResponse[GoalMilestoneResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_milestone(
    goal_id: UUID,
    milestone_data: GoalMilestoneCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Create a milestone for a life goal.

    - **title**: Milestone title (required)
    - **description**: Optional description
    - **order_index**: Order in the milestone sequence
    - **target_date**: Optional target completion date
    """
    service = GoalService(db)
    milestone = await service.create_milestone(goal_id, current_user.id, milestone_data)

    return APIResponse(
        data=GoalMilestoneResponse.model_validate(milestone),
        message="Milestone created successfully",
    )


@router.get(
    "/{goal_id}/milestones", response_model=APIResponse[list[GoalMilestoneResponse]]
)
async def get_goal_milestones(
    goal_id: UUID,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get milestones for a goal."""
    service = GoalService(db)
    skip = (page - 1) * limit
    milestones = await service.get_goal_milestones(
        goal_id, current_user.id, skip, limit
    )

    return APIResponse(
        data=[GoalMilestoneResponse.model_validate(m) for m in milestones],
        message="Milestones retrieved successfully",
    )


@router.put(
    "/{goal_id}/milestones/{milestone_id}",
    response_model=APIResponse[GoalMilestoneResponse],
)
async def update_milestone(
    goal_id: UUID,
    milestone_id: UUID,
    milestone_data: GoalMilestoneUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Update a milestone.

    All fields are optional. Only provided fields will be updated.
    """
    service = GoalService(db)
    milestone = await service.update_milestone(
        milestone_id, goal_id, current_user.id, milestone_data
    )

    return APIResponse(
        data=GoalMilestoneResponse.model_validate(milestone),
        message="Milestone updated successfully",
    )


@router.delete(
    "/{goal_id}/milestones/{milestone_id}",
    response_model=APIResponse[dict],
    status_code=status.HTTP_200_OK,
)
async def delete_milestone(
    goal_id: UUID,
    milestone_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a milestone."""
    service = GoalService(db)
    deleted = await service.delete_milestone(milestone_id, goal_id, current_user.id)

    return APIResponse(
        data={"deleted": deleted}, message="Milestone deleted successfully"
    )
