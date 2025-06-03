from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from app.domain.services.user_service import UserService
from app.presentation.api.dependencies import get_user_service
from app.presentation.schemas.user import UserCreate, UserResponse, UserUpdate

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate, user_service: UserService = Depends(get_user_service)
) -> UserResponse:
    """Create a new user"""
    user = await user_service.create_user(
        username=user_data.username, email=user_data.email, password=user_data.password
    )
    return UserResponse.model_validate(user)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int, user_service: UserService = Depends(get_user_service)
) -> UserResponse:
    """Get user by ID"""
    user = await user_service.get_user_by_id(user_id)
    return UserResponse.model_validate(user)


@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    user_service: UserService = Depends(get_user_service),
) -> List[UserResponse]:
    """Get all users with pagination"""
    users = await user_service.get_all_users(skip=skip, limit=limit)
    return [UserResponse.model_validate(user) for user in users]


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    """Update user"""
    user = await user_service.update_user(
        user_id=user_id, username=user_data.username, email=user_data.email
    )
    return UserResponse.model_validate(user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int, user_service: UserService = Depends(get_user_service)
):
    """Delete user"""
    await user_service.delete_user(user_id)


@router.get("/username/{username}", response_model=UserResponse)
async def get_user_by_username(
    username: str, user_service: UserService = Depends(get_user_service)
) -> UserResponse:
    """Get user by username"""
    user = await user_service.get_user_by_username(username)
    return UserResponse.model_validate(user)
