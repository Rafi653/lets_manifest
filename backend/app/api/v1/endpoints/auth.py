"""
Authentication endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.common import APIResponse
from app.schemas.user import LoginRequest, TokenResponse, UserCreate, UserResponse
from app.services.user_service import UserService

router = APIRouter()


@router.post("/register", response_model=APIResponse[UserResponse], status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Register a new user.
    
    - **email**: Valid email address
    - **username**: Unique username (3-100 characters)
    - **password**: Strong password (min 8 characters)
    - **first_name**: Optional first name
    - **last_name**: Optional last name
    """
    service = UserService(db)
    user = await service.create_user(user_data)
    
    return APIResponse(
        data=UserResponse.model_validate(user),
        message="User registered successfully"
    )


@router.post("/login", response_model=APIResponse[TokenResponse])
async def login(
    credentials: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Login and get JWT tokens.
    
    - **email**: User's email address
    - **password**: User's password
    
    Returns access and refresh tokens.
    """
    service = UserService(db)
    token_response = await service.login(credentials.email, credentials.password)
    
    return APIResponse(
        data=token_response,
        message="Login successful"
    )


@router.post("/logout", response_model=APIResponse[dict])
async def logout():
    """
    Logout user (client should discard tokens).
    
    Since we're using JWT, logout is handled client-side by discarding tokens.
    This endpoint is provided for consistency and future enhancements.
    """
    return APIResponse(
        data={"logged_out": True},
        message="Logout successful"
    )
