from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status

from app.domain.services.auth_service import SupabaseAuthService
from app.presentation.api.dependencies import get_supabase_auth_service
from app.presentation.schemas.auth import (
    SignUpRequest,
    SignInRequest,
    AuthResponse,
    RefreshTokenRequest,
    ResetPasswordRequest,
    UpdateProfileRequest,
)
from app.core.auth import get_current_user
from app.presentation.schemas.user import UserResponse


router = APIRouter()


@router.post(
    "/signup", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED
)
async def sign_up(
    user_data: SignUpRequest,
    auth_service: SupabaseAuthService = Depends(get_supabase_auth_service),
):
    """Sign up a new user with Supabase Auth"""
    try:
        user_metadata = {}
        if user_data.username:
            user_metadata["username"] = user_data.username
        if user_data.full_name:
            user_metadata["full_name"] = user_data.full_name

        result = await auth_service.sign_up(
            email=user_data.email,
            password=user_data.password,
            user_metadata=user_metadata,
        )

        return {
            "message": "User created successfully",
            "user": result["user"],
            "session": result["session"],
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/signin", response_model=Dict[str, Any])
async def sign_in(
    credentials: SignInRequest,
    auth_service: SupabaseAuthService = Depends(get_supabase_auth_service),
):
    try:
        user = await auth_service.sign_in(
            email=credentials.email, password=credentials.password
        )

        return UserResponse.model_validate(user)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
