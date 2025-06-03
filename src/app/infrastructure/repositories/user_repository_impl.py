from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.database.models import UserModel


class UserRepositoryImpl(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _model_to_entity(self, model: UserModel) -> User:
        return User(
            id=model.id,
            username=model.username,
            email=model.email,
            hashed_password=model.hashed_password,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _entity_to_model(self, user: User) -> UserModel:
        model_data = {
            "username": user.username,
            "email": user.email,
            "hashed_password": user.hashed_password,
            "is_active": user.is_active,
        }

        if user.id is not None:
            model_data["id"] = user.id
        if user.created_at is not None:
            model_data["created_at"] = user.created_at
        if user.updated_at is not None:
            model_data["updated_at"] = user.updated_at

        return UserModel(**model_data)

    async def create(self, user: User) -> User:
        model = self._entity_to_model(user)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._model_to_entity(model)

    async def get_by_id(self, user_id: int) -> Optional[User]:
        try:
            stmt = select(UserModel).where(UserModel.id == user_id)
            result = await self.session.execute(stmt)
            model = result.scalar_one()
            return self._model_to_entity(model)
        except NoResultFound:
            return None

    async def get_by_username(self, username: str) -> Optional[User]:
        try:
            stmt = select(UserModel).where(UserModel.username == username)
            result = await self.session.execute(stmt)
            model = result.scalar_one()
            return self._model_to_entity(model)
        except NoResultFound:
            return None

    async def get_by_email(self, email: str) -> Optional[User]:
        try:
            stmt = select(UserModel).where(UserModel.email == email)
            result = await self.session.execute(stmt)
            model = result.scalar_one()
            return self._model_to_entity(model)
        except NoResultFound:
            return None

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        stmt = select(UserModel).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self._model_to_entity(model) for model in models]

    async def update(self, user: User) -> User:
        stmt = select(UserModel).where(UserModel.id == user.id)
        result = await self.session.execute(stmt)
        model = result.scalar_one()

        model.username = user.username
        model.email = user.email
        model.hashed_password = user.hashed_password
        model.is_active = user.is_active
        model.updated_at = user.updated_at

        await self.session.commit()
        await self.session.refresh(model)
        return self._model_to_entity(model)

    async def delete(self, user_id: int) -> bool:
        try:
            stmt = select(UserModel).where(UserModel.id == user_id)
            result = await self.session.execute(stmt)
            model = result.scalar_one()
            await self.session.delete(model)
            await self.session.commit()
            return True
        except NoResultFound:
            return False
