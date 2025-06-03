from typing import Optional, Dict, Any
from supabase import Client
from app.core.exceptions import UserNotFoundException, UserAlreadyExistsException


class SupabaseAuthService:
    def __init__(self, supabase: Client):
        self.supabase = supabase

    async def sign_up(
        self, email: str, password: str, user_metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Sign up a new user with Supabase Auth"""
        try:
            response = self.supabase.auth.sign_up(
                {
                    "email": email,
                    "password": password,
                    "options": {"data": user_metadata or {}},
                }
            )

            if response.user:
                return {"user": response.user, "session": response.session}
            else:
                raise UserAlreadyExistsException("User registration failed")

        except Exception as e:
            if "already registered" in str(e).lower():
                raise UserAlreadyExistsException("User with this email already exists")
            raise Exception(f"Registration failed: {str(e)}")

    async def sign_in(self, email: str, password: str) -> Dict[str, Any]:
        """Sign in user with Supabase Auth"""
        try:
            response = self.supabase.auth.sign_in_with_password(
                {"email": email, "password": password}
            )

            if response.user and response.session:
                return {
                    "user": response.user,
                    "session": response.session,
                    "access_token": response.session.access_token,
                    "refresh_token": response.session.refresh_token,
                }
            else:
                raise UserNotFoundException("Invalid credentials")

        except Exception as e:
            if "invalid" in str(e).lower():
                raise UserNotFoundException("Invalid email or password")
            raise Exception(f"Sign in failed: {str(e)}")

    async def sign_out(self) -> bool:
        """Sign out current user"""
        try:
            self.supabase.auth.sign_out()
            return True
        except Exception:
            return False
