"""
Habit endpoints.
"""

from datetime import date
from typing import Optional
from uuid import UUID
import math

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.common import APIResponse, PaginatedResponse
from app.schemas.habit import (
    HabitCreate,
    HabitUpdate,
    HabitResponse,
    HabitEntryCreate,
    HabitEntryResponse,
)
from app.services.module_services import HabitService

router = APIRouter()


@router.post(
    "", response_model=APIResponse[HabitResponse], status_code=status.HTTP_201_CREATED
)
async def create_habit(
    habit_data: HabitCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new habit."""
    service = HabitService(db)
    habit = await service.create_habit(current_user.id, habit_data)
    return APIResponse(
        data=HabitResponse.model_validate(habit), message="Habit created successfully"
    )


@router.get("", response_model=APIResponse[PaginatedResponse[HabitResponse]])
async def list_habits(
    is_active: Optional[bool] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all habits for the current user."""
    service = HabitService(db)
    skip = (page - 1) * limit
    habits, total = await service.get_user_habits(
        current_user.id, is_active, skip, limit
    )

    return APIResponse(
        data=PaginatedResponse(
            items=[HabitResponse.model_validate(h) for h in habits],
            total=total,
            page=page,
            limit=limit,
            total_pages=math.ceil(total / limit) if total > 0 else 0,
        ),
        message="Habits retrieved successfully",
    )


@router.get("/{habit_id}", response_model=APIResponse[HabitResponse])
async def get_habit(
    habit_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a specific habit by ID."""
    service = HabitService(db)
    habit = await service.get_habit(habit_id, current_user.id)
    return APIResponse(
        data=HabitResponse.model_validate(habit), message="Habit retrieved successfully"
    )


@router.put("/{habit_id}", response_model=APIResponse[HabitResponse])
async def update_habit(
    habit_id: UUID,
    habit_data: HabitUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update a habit."""
    service = HabitService(db)
    habit = await service.update_habit(habit_id, current_user.id, habit_data)
    return APIResponse(
        data=HabitResponse.model_validate(habit), message="Habit updated successfully"
    )


@router.delete("/{habit_id}", response_model=APIResponse[dict])
async def delete_habit(
    habit_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a habit."""
    service = HabitService(db)
    deleted = await service.delete_habit(habit_id, current_user.id)
    return APIResponse(data={"deleted": deleted}, message="Habit deleted successfully")


@router.post(
    "/{habit_id}/entries",
    response_model=APIResponse[HabitEntryResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_habit_entry(
    habit_id: UUID,
    entry_data: HabitEntryCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a habit entry."""
    service = HabitService(db)
    entry = await service.create_entry(habit_id, current_user.id, entry_data)
    return APIResponse(
        data=HabitEntryResponse.model_validate(entry),
        message="Habit entry created successfully",
    )


@router.get("/{habit_id}/entries", response_model=APIResponse[list[HabitEntryResponse]])
async def get_habit_entries(
    habit_id: UUID,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get entries for a habit."""
    service = HabitService(db)
    skip = (page - 1) * limit
    entries = await service.get_habit_entries(habit_id, current_user.id, skip, limit)
    return APIResponse(
        data=[HabitEntryResponse.model_validate(e) for e in entries],
        message="Habit entries retrieved successfully",
    )


@router.post("/{habit_id}/reset-streak", response_model=APIResponse[HabitResponse])
async def reset_habit_streak(
    habit_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Reset a habit's streak to zero."""
    service = HabitService(db)
    habit = await service.reset_habit_streak(habit_id, current_user.id)
    return APIResponse(
        data=HabitResponse.model_validate(habit),
        message="Habit streak reset successfully",
    )


@router.post(
    "/{habit_id}/recover-streak",
    response_model=APIResponse[HabitEntryResponse],
    status_code=status.HTTP_201_CREATED,
)
async def recover_habit_streak(
    habit_id: UUID,
    recovery_date: date = Query(..., description="Date to recover the streak for"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Recover a broken streak by creating an entry for a missed date.
    Only allowed within the grace period.
    """
    service = HabitService(db)
    entry = await service.recover_streak(habit_id, current_user.id, recovery_date)
    return APIResponse(
        data=HabitEntryResponse.model_validate(entry),
        message="Streak recovered successfully",
    )
