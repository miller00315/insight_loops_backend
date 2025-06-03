from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from supabase import Client

from app.core.dependencies import get_db
from app.core.supabase import get_supabase_client
from app.domain.services.user_service import UserService
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    user_repository = UserRepositoryImpl(db)
    return UserService(user_repository)


def get_supabase_user_service(
    supabase: Client = Depends(get_supabase_client),
) -> UserService:
    from app.infrastructure.supabase.supabase_repository import SupabaseUserRepository

    user_repository = SupabaseUserRepository(supabase)
    return UserService(user_repository)


def get_supabase_auth_service(supabase: Client = Depends(get_supabase_client)):
    from app.domain.services.auth_service import SupabaseAuthService

    return SupabaseAuthService(supabase)


def get_realtime_service(supabase: Client = Depends(get_supabase_client)):
    from app.infrastructure.supabase.realtime_service import SupabaseRealtimeService

    return SupabaseRealtimeService(supabase)
