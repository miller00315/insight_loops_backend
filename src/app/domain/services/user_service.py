from typing import List, Optional
from passlib.context import CryptContext

from app.core.exceptions import UserAlreadyExistsException, UserNotFoundException
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.pwd_context = CryptContext(
            schemes=["brcrypt"],
            deprecated="auto",
        )

    def _hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    async def create_user(self, email: str, password: str) -> User:
        # Check if user already exists
        existing_user = await self.user_repository.get_by_email(email)
        if existing_user:
            raise UserAlreadyExistsException(
                f"User with email '{email}' already exists"
            )

        # Create new user
        hashed_password = self._hash_password(password)
        user = User(
            id=None,
            email=email,
            hashed_password=hashed_password,
            is_active=True,
        )

        return await self.user_repository.create(user)

    async def get_user_by_email(self, email: str) -> User:
        user = await self.user_repository.get_by_email(email)
        if not user:
            raise UserNotFoundException(f"User with email '{email}' not found")
        return user

    async def get_user_by_id(self, user_id: int) -> User:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"User with id {user_id} not found")
        return user

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        try:
            user = await self.get_user_by_email(email)
            if not self._verify_password(password, user.hashed_password):
                return None
            return user
        except UserNotFoundException:
            return None

    async def delete_user(self, user_id: int) -> bool:
        user = await self.get_user_by_id(
            user_id
        )  # This will raise if user doesn't exist
        return await self.user_repository.delete(user_id)
