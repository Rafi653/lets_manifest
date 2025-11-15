"""
Progress snapshot endpoints.
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
from app.schemas.progress_snapshot import ProgressSnapshotCreate, ProgressSnapshotUpdate, ProgressSnapshotResponse
from app.services.module_services import ProgressSnapshotService

router = APIRouter()


@router.post("", response_model=APIResponse[ProgressSnapshotResponse], status_code=status.HTTP_201_CREATED)
async def create_progress_snapshot(
    snapshot_data: ProgressSnapshotCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a progress snapshot."""
    service = ProgressSnapshotService(db)
    snapshot = await service.create_snapshot(current_user.id, snapshot_data)
    return APIResponse(
        data=ProgressSnapshotResponse.model_validate(snapshot),
        message="Progress snapshot created successfully"
    )


@router.get("", response_model=APIResponse[PaginatedResponse[ProgressSnapshotResponse]])
async def list_progress_snapshots(
    snapshot_type: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all progress snapshots for the current user."""
    service = ProgressSnapshotService(db)
    skip = (page - 1) * limit
    snapshots, total = await service.get_user_snapshots(
        current_user.id, snapshot_type, skip, limit
    )
    
    return APIResponse(
        data=PaginatedResponse(
            items=[ProgressSnapshotResponse.model_validate(s) for s in snapshots],
            total=total,
            page=page,
            limit=limit,
            total_pages=math.ceil(total / limit) if total > 0 else 0
        ),
        message="Progress snapshots retrieved successfully"
    )


@router.get("/{snapshot_id}", response_model=APIResponse[ProgressSnapshotResponse])
async def get_progress_snapshot(
    snapshot_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a specific progress snapshot by ID."""
    service = ProgressSnapshotService(db)
    snapshot = await service.get_snapshot(snapshot_id, current_user.id)
    return APIResponse(
        data=ProgressSnapshotResponse.model_validate(snapshot),
        message="Progress snapshot retrieved successfully"
    )


@router.put("/{snapshot_id}", response_model=APIResponse[ProgressSnapshotResponse])
async def update_progress_snapshot(
    snapshot_id: UUID,
    snapshot_data: ProgressSnapshotUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update a progress snapshot."""
    service = ProgressSnapshotService(db)
    snapshot = await service.update_snapshot(snapshot_id, current_user.id, snapshot_data)
    return APIResponse(
        data=ProgressSnapshotResponse.model_validate(snapshot),
        message="Progress snapshot updated successfully"
    )


@router.delete("/{snapshot_id}", response_model=APIResponse[dict])
async def delete_progress_snapshot(
    snapshot_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a progress snapshot."""
    service = ProgressSnapshotService(db)
    deleted = await service.delete_snapshot(snapshot_id, current_user.id)
    return APIResponse(
        data={"deleted": deleted},
        message="Progress snapshot deleted successfully"
    )
