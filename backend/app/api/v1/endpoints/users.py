"""
User endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.common import APIResponse
from app.schemas.user import UserResponse, UserUpdate
from app.services.user_service import UserService

router = APIRouter()


@router.get("/me", response_model=APIResponse[UserResponse])
async def get_current_user_profile(
    current_user: User = Depends(get_current_user),
):
    """
    Get current user profile.
    
    Requires authentication.
    """
    return APIResponse(
        data=UserResponse.model_validate(current_user),
        message="User profile retrieved successfully"
    )


@router.put("/me", response_model=APIResponse[UserResponse])
async def update_current_user_profile(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Update current user profile.
    
    - **first_name**: Optional first name
    - **last_name**: Optional last name
    - **avatar_url**: Optional avatar URL
    - **bio**: Optional bio text
    - **timezone**: Optional timezone
    
    Requires authentication.
    """
    service = UserService(db)
    updated_user = await service.update_user(current_user.id, user_data)
    
    return APIResponse(
        data=UserResponse.model_validate(updated_user),
        message="User profile updated successfully"
    )


@router.delete("/me", response_model=APIResponse[dict])
async def delete_current_user_account(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Delete current user account.
    
    This action is irreversible.
    Requires authentication.
    """
    service = UserService(db)
    deleted = await service.delete_user(current_user.id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete user account"
        )
    
    return APIResponse(
        data={"deleted": True},
        message="User account deleted successfully"
    )
