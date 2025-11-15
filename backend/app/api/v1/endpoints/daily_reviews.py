"""
Daily review endpoints.
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
from app.schemas.daily_review import DailyReviewCreate, DailyReviewUpdate, DailyReviewResponse
from app.services.module_services import DailyReviewService

router = APIRouter()


@router.post("", response_model=APIResponse[DailyReviewResponse], status_code=status.HTTP_201_CREATED)
async def create_daily_review(
    review_data: DailyReviewCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a daily review."""
    service = DailyReviewService(db)
    review = await service.create_review(current_user.id, review_data)
    return APIResponse(
        data=DailyReviewResponse.model_validate(review),
        message="Daily review created successfully"
    )


@router.get("", response_model=APIResponse[PaginatedResponse[DailyReviewResponse]])
async def list_daily_reviews(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all daily reviews for the current user."""
    service = DailyReviewService(db)
    skip = (page - 1) * limit
    reviews, total = await service.get_user_reviews(
        current_user.id, start_date, end_date, skip, limit
    )
    
    return APIResponse(
        data=PaginatedResponse(
            items=[DailyReviewResponse.model_validate(r) for r in reviews],
            total=total,
            page=page,
            limit=limit,
            total_pages=math.ceil(total / limit) if total > 0 else 0
        ),
        message="Daily reviews retrieved successfully"
    )


@router.get("/{review_id}", response_model=APIResponse[DailyReviewResponse])
async def get_daily_review(
    review_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a specific daily review by ID."""
    service = DailyReviewService(db)
    review = await service.get_review(review_id, current_user.id)
    return APIResponse(
        data=DailyReviewResponse.model_validate(review),
        message="Daily review retrieved successfully"
    )


@router.put("/{review_id}", response_model=APIResponse[DailyReviewResponse])
async def update_daily_review(
    review_id: UUID,
    review_data: DailyReviewUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update a daily review."""
    service = DailyReviewService(db)
    review = await service.update_review(review_id, current_user.id, review_data)
    return APIResponse(
        data=DailyReviewResponse.model_validate(review),
        message="Daily review updated successfully"
    )


@router.delete("/{review_id}", response_model=APIResponse[dict])
async def delete_daily_review(
    review_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a daily review."""
    service = DailyReviewService(db)
    deleted = await service.delete_review(review_id, current_user.id)
    return APIResponse(
        data={"deleted": deleted},
        message="Daily review deleted successfully"
    )
