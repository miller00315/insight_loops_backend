from typing import List, Optional, Dict, Any
from supabase import Client
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository


class SupabaseUserRepository(UserRepository):
    def __init__(self, supabase: Client):
        self.supabase = supabase
        self.table_name = "users"

    def _dict_to_entity(self, data: Dict[str, Any]) -> User:
        """Convert Supabase dict to User entity"""
        return User(
            id=data.get("id"),
            username=data.get("username"),
            email=data.get("email"),
            hashed_password=data.get("hashed_password", ""),
            is_active=data.get("is_active", True),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )

    def _entity_to_dict(self, user: User) -> Dict[str, Any]:
        """Convert User entity to dict for Supabase"""
        data = {
            "username": user.username,
            "email": user.email,
            "hashed_password": user.hashed_password,
            "is_active": user.is_active,
        }

        if user.id is not None:
            data["id"] = user.id
        if user.created_at is not None:
            data["created_at"] = user.created_at.isoformat()
        if user.updated_at is not None:
            data["updated_at"] = user.updated_at.isoformat()

        return data

    async def create(self, user: User) -> User:
        """Create user in Supabase"""
        try:
            data = self._entity_to_dict(user)
            response = self.supabase.table(self.table_name).insert(data).execute()

            if response.data:
                return self._dict_to_entity(response.data[0])
            else:
                raise Exception("Failed to create user")
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        try:
            response = (
                self.supabase.table(self.table_name)
                .select("*")
                .eq("id", user_id)
                .execute()
            )

            if response.data:
                return self._dict_to_entity(response.data[0])
            return None
        except Exception:
            return None

    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        try:
            response = (
                self.supabase.table(self.table_name)
                .select("*")
                .eq("username", username)
                .execute()
            )

            if response.data:
                return self._dict_to_entity(response.data[0])
            return None
        except Exception:
            return None

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        try:
            response = (
                self.supabase.table(self.table_name)
                .select("*")
                .eq("email", email)
                .execute()
            )

            if response.data:
                return self._dict_to_entity(response.data[0])
            return None
        except Exception:
            return None

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination"""
        try:
            response = (
                self.supabase.table(self.table_name)
                .select("*")
                .range(skip, skip + limit - 1)
                .execute()
            )

            return [self._dict_to_entity(item) for item in response.data]
        except Exception:
            return []

    async def update(self, user: User) -> User:
        """Update user"""
        try:
            data = self._entity_to_dict(user)
            response = (
                self.supabase.table(self.table_name)
                .update(data)
                .eq("id", user.id)
                .execute()
            )

            if response.data:
                return self._dict_to_entity(response.data[0])
            else:
                raise Exception("Failed to update user")
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")

    async def delete(self, user_id: int) -> bool:
        """Delete user"""
        try:
            response = (
                self.supabase.table(self.table_name)
                .delete()
                .eq("id", user_id)
                .execute()
            )

            return len(response.data) > 0
        except Exception:
            return False
