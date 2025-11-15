"""
Notification endpoints.
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.common import APIResponse, PaginatedResponse
from app.schemas.notification import (
    NotificationCreate,
    NotificationResponse,
    NotificationSettingsCreate,
    NotificationSettingsResponse,
    NotificationSettingsUpdate,
    NotificationUpdate,
)
from app.services.notification_service import NotificationService
import math

router = APIRouter()


@router.post(
    "",
    response_model=APIResponse[NotificationResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_notification(
    notification_data: NotificationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new notification.

    - **title**: Notification title (required)
    - **message**: Optional message
    - **notification_type**: Type of notification (reminder/goal_deadline/goal_completed/system)
    - **scheduled_time**: When to send the notification
    - **goal_id**: Optional related goal ID
    """
    service = NotificationService(db)
    notification = await service.create_notification(current_user.id, notification_data)

    return APIResponse(
        data=NotificationResponse.model_validate(notification),
        message="Notification created successfully",
    )


@router.get("", response_model=APIResponse[PaginatedResponse[NotificationResponse]])
async def list_notifications(
    is_read: Optional[bool] = Query(None, description="Filter by read status"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    List all notifications for the current user with pagination and filtering.

    Query parameters:
    - **is_read**: Filter by read status (true/false)
    - **page**: Page number (default: 1)
    - **limit**: Items per page (default: 20, max: 100)
    """
    service = NotificationService(db)
    skip = (page - 1) * limit
    notifications, total = await service.get_user_notifications(
        current_user.id, is_read, skip, limit
    )

    notification_responses = [
        NotificationResponse.model_validate(notification)
        for notification in notifications
    ]

    return APIResponse(
        data=PaginatedResponse(
            items=notification_responses,
            total=total,
            page=page,
            limit=limit,
            total_pages=math.ceil(total / limit) if total > 0 else 0,
        ),
        message="Notifications retrieved successfully",
    )


@router.get("/{notification_id}", response_model=APIResponse[NotificationResponse])
async def get_notification(
    notification_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a specific notification by ID."""
    service = NotificationService(db)
    notification = await service.get_notification(notification_id, current_user.id)

    return APIResponse(
        data=NotificationResponse.model_validate(notification),
        message="Notification retrieved successfully",
    )


@router.put("/{notification_id}", response_model=APIResponse[NotificationResponse])
async def update_notification(
    notification_id: UUID,
    notification_data: NotificationUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Update a notification.

    All fields are optional. Only provided fields will be updated.
    """
    service = NotificationService(db)
    notification = await service.update_notification(
        notification_id, current_user.id, notification_data
    )

    return APIResponse(
        data=NotificationResponse.model_validate(notification),
        message="Notification updated successfully",
    )


@router.post(
    "/{notification_id}/read", response_model=APIResponse[NotificationResponse]
)
async def mark_notification_as_read(
    notification_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Mark a notification as read."""
    service = NotificationService(db)
    notification = await service.mark_as_read(notification_id, current_user.id)

    return APIResponse(
        data=NotificationResponse.model_validate(notification),
        message="Notification marked as read",
    )


@router.delete(
    "/{notification_id}",
    response_model=APIResponse[dict],
    status_code=status.HTTP_200_OK,
)
async def delete_notification(
    notification_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a notification."""
    service = NotificationService(db)
    deleted = await service.delete_notification(notification_id, current_user.id)

    return APIResponse(
        data={"deleted": deleted}, message="Notification deleted successfully"
    )


# Notification Settings endpoints


@router.get(
    "/settings/me", response_model=APIResponse[NotificationSettingsResponse]
)
async def get_my_notification_settings(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get notification settings for the current user."""
    service = NotificationService(db)
    settings = await service.get_user_settings(current_user.id)

    return APIResponse(
        data=NotificationSettingsResponse.model_validate(settings),
        message="Notification settings retrieved successfully",
    )


@router.post(
    "/settings",
    response_model=APIResponse[NotificationSettingsResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_notification_settings(
    settings_data: NotificationSettingsCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create notification settings for the current user."""
    service = NotificationService(db)
    settings = await service.create_settings(current_user.id, settings_data)

    return APIResponse(
        data=NotificationSettingsResponse.model_validate(settings),
        message="Notification settings created successfully",
    )


@router.put(
    "/settings/me", response_model=APIResponse[NotificationSettingsResponse]
)
async def update_my_notification_settings(
    settings_data: NotificationSettingsUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update notification settings for the current user."""
    service = NotificationService(db)
    settings = await service.update_settings(current_user.id, settings_data)

    return APIResponse(
        data=NotificationSettingsResponse.model_validate(settings),
        message="Notification settings updated successfully",
    )
