"""
Workout endpoints.
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
from app.schemas.workout import WorkoutCreate, WorkoutUpdate, WorkoutResponse
from app.services.module_services import WorkoutService

router = APIRouter()


@router.post("", response_model=APIResponse[WorkoutResponse], status_code=status.HTTP_201_CREATED)
async def create_workout(
    workout_data: WorkoutCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a workout with exercises."""
    service = WorkoutService(db)
    workout = await service.create_workout(current_user.id, workout_data)
    return APIResponse(
        data=WorkoutResponse.model_validate(workout),
        message="Workout created successfully"
    )


@router.get("", response_model=APIResponse[PaginatedResponse[WorkoutResponse]])
async def list_workouts(
    workout_type: Optional[str] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all workouts for the current user."""
    service = WorkoutService(db)
    skip = (page - 1) * limit
    workouts, total = await service.get_user_workouts(
        current_user.id, workout_type, start_date, end_date, skip, limit
    )
    
    return APIResponse(
        data=PaginatedResponse(
            items=[WorkoutResponse.model_validate(w) for w in workouts],
            total=total,
            page=page,
            limit=limit,
            total_pages=math.ceil(total / limit) if total > 0 else 0
        ),
        message="Workouts retrieved successfully"
    )


@router.get("/{workout_id}", response_model=APIResponse[WorkoutResponse])
async def get_workout(
    workout_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a specific workout by ID."""
    service = WorkoutService(db)
    workout = await service.get_workout(workout_id, current_user.id)
    return APIResponse(
        data=WorkoutResponse.model_validate(workout),
        message="Workout retrieved successfully"
    )


@router.put("/{workout_id}", response_model=APIResponse[WorkoutResponse])
async def update_workout(
    workout_id: UUID,
    workout_data: WorkoutUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update a workout."""
    service = WorkoutService(db)
    workout = await service.update_workout(workout_id, current_user.id, workout_data)
    return APIResponse(
        data=WorkoutResponse.model_validate(workout),
        message="Workout updated successfully"
    )


@router.delete("/{workout_id}", response_model=APIResponse[dict])
async def delete_workout(
    workout_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a workout."""
    service = WorkoutService(db)
    deleted = await service.delete_workout(workout_id, current_user.id)
    return APIResponse(
        data={"deleted": deleted},
        message="Workout deleted successfully"
    )
