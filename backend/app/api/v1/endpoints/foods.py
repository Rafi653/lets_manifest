"""
Food tracking endpoints.
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
from app.schemas.food import FoodCreate, FoodUpdate, FoodResponse
from app.services.module_services import FoodService

router = APIRouter()


@router.post(
    "", response_model=APIResponse[FoodResponse], status_code=status.HTTP_201_CREATED
)
async def create_food(
    food_data: FoodCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a food entry."""
    service = FoodService(db)
    food = await service.create_food(current_user.id, food_data)
    return APIResponse(
        data=FoodResponse.model_validate(food),
        message="Food entry created successfully",
    )


@router.get("", response_model=APIResponse[PaginatedResponse[FoodResponse]])
async def list_foods(
    meal_type: Optional[str] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all food entries for the current user."""
    service = FoodService(db)
    skip = (page - 1) * limit
    foods, total = await service.get_user_foods(
        current_user.id, meal_type, start_date, end_date, skip, limit
    )

    return APIResponse(
        data=PaginatedResponse(
            items=[FoodResponse.model_validate(f) for f in foods],
            total=total,
            page=page,
            limit=limit,
            total_pages=math.ceil(total / limit) if total > 0 else 0,
        ),
        message="Food entries retrieved successfully",
    )


@router.get("/{food_id}", response_model=APIResponse[FoodResponse])
async def get_food(
    food_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a specific food entry by ID."""
    service = FoodService(db)
    food = await service.get_food(food_id, current_user.id)
    return APIResponse(
        data=FoodResponse.model_validate(food),
        message="Food entry retrieved successfully",
    )


@router.put("/{food_id}", response_model=APIResponse[FoodResponse])
async def update_food(
    food_id: UUID,
    food_data: FoodUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update a food entry."""
    service = FoodService(db)
    food = await service.update_food(food_id, current_user.id, food_data)
    return APIResponse(
        data=FoodResponse.model_validate(food),
        message="Food entry updated successfully",
    )


@router.delete("/{food_id}", response_model=APIResponse[dict])
async def delete_food(
    food_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a food entry."""
    service = FoodService(db)
    deleted = await service.delete_food(food_id, current_user.id)
    return APIResponse(
        data={"deleted": deleted}, message="Food entry deleted successfully"
    )
