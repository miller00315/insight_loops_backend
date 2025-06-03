from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any

from app.core.exceptions import UserNotFoundException


class SignUpRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, max_length=100)


class SignInRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: Dict[str, Any]


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class ResetPasswordRequest(BaseModel):
    email: EmailStr


class UpdateProfileRequest(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, max_length=100)
    avatar_url: Optional[str] = None

    async def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """Refresh access token"""
        try:
            response = self.supabase.auth.refresh_session(refresh_token)
            if response.session:
                return {
                    "session": response.session,
                    "access_token": response.session.access_token,
                    "refresh_token": response.session.refresh_token,
                }
            else:
                raise Exception("Token refresh failed")
        except Exception as e:
            raise Exception(f"Token refresh failed: {str(e)}")

    async def get_user(self, access_token: str) -> Dict[str, Any]:
        """Get user details from access token"""
        try:
            response = self.supabase.auth.get_user(access_token)
            if response.user:
                return response.user
            else:
                raise UserNotFoundException("User not found")
        except Exception as e:
            raise UserNotFoundException(f"Failed to get user: {str(e)}")

    async def update_user(
        self, access_token: str, user_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update user profile"""
        try:
            # Set the session token
            self.supabase.auth.set_session(access_token, "")

            response = self.supabase.auth.update_user({"data": user_data})

            if response.user:
                return response.user
            else:
                raise Exception("User update failed")
        except Exception as e:
            raise Exception(f"User update failed: {str(e)}")

    async def reset_password(self, email: str) -> bool:
        """Send password reset email"""
        try:
            self.supabase.auth.reset_password_email(email)
            return True
        except Exception:
            return False
