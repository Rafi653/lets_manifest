"""
Blog entry endpoints.
"""

from typing import Optional
from uuid import UUID
import math

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.common import APIResponse, PaginatedResponse
from app.schemas.blog_entry import BlogEntryCreate, BlogEntryUpdate, BlogEntryResponse
from app.services.module_services import BlogEntryService

router = APIRouter()


@router.post(
    "",
    response_model=APIResponse[BlogEntryResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_blog_entry(
    entry_data: BlogEntryCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a blog entry."""
    service = BlogEntryService(db)
    entry = await service.create_blog_entry(current_user.id, entry_data)
    return APIResponse(
        data=BlogEntryResponse.model_validate(entry),
        message="Blog entry created successfully",
    )


@router.get("", response_model=APIResponse[PaginatedResponse[BlogEntryResponse]])
async def list_blog_entries(
    status_filter: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all blog entries for the current user."""
    service = BlogEntryService(db)
    skip = (page - 1) * limit
    entries, total = await service.get_user_blog_entries(
        current_user.id, status_filter, skip, limit
    )

    return APIResponse(
        data=PaginatedResponse(
            items=[BlogEntryResponse.model_validate(e) for e in entries],
            total=total,
            page=page,
            limit=limit,
            total_pages=math.ceil(total / limit) if total > 0 else 0,
        ),
        message="Blog entries retrieved successfully",
    )


@router.get("/{entry_id}", response_model=APIResponse[BlogEntryResponse])
async def get_blog_entry(
    entry_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a specific blog entry by ID."""
    service = BlogEntryService(db)
    entry = await service.get_blog_entry(entry_id, current_user.id)
    return APIResponse(
        data=BlogEntryResponse.model_validate(entry),
        message="Blog entry retrieved successfully",
    )


@router.put("/{entry_id}", response_model=APIResponse[BlogEntryResponse])
async def update_blog_entry(
    entry_id: UUID,
    entry_data: BlogEntryUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update a blog entry."""
    service = BlogEntryService(db)
    entry = await service.update_blog_entry(entry_id, current_user.id, entry_data)
    return APIResponse(
        data=BlogEntryResponse.model_validate(entry),
        message="Blog entry updated successfully",
    )


@router.delete("/{entry_id}", response_model=APIResponse[dict])
async def delete_blog_entry(
    entry_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a blog entry."""
    service = BlogEntryService(db)
    deleted = await service.delete_blog_entry(entry_id, current_user.id)
    return APIResponse(
        data={"deleted": deleted}, message="Blog entry deleted successfully"
    )


@router.post(
    "/generate-from-review/{review_id}",
    response_model=APIResponse[BlogEntryResponse],
    status_code=status.HTTP_201_CREATED,
)
async def generate_blog_from_review(
    review_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Generate a blog entry from a daily review."""
    from app.services.module_services import DailyReviewService
    
    blog_service = BlogEntryService(db)
    review_service = DailyReviewService(db)
    
    # Get the daily review
    review = await review_service.get_review(review_id, current_user.id)
    
    # Generate blog entry from review
    entry = await blog_service.generate_blog_from_review(current_user.id, review)
    
    return APIResponse(
        data=BlogEntryResponse.model_validate(entry),
        message="Blog entry generated successfully from daily review",
    )
