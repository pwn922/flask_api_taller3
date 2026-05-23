import uuid
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.domain.user import User, UserRepository
from app.users.infrastructure.databases.postgresql.models.user_model import (
    User as UserModel,
)


class PostgreSQLUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_entity(self, model: UserModel) -> User:
        return User(
            id=model.id,
            username=model.username,
            email=model.email,
            hashed_password=model.hashed_password,
        )

    async def get_all(self) -> List[User]:
        result = await self.session.execute(select(UserModel))
        models = result.scalars().all()
        return [self._to_entity(m) for m in models]

    async def get_by_id(self, id: uuid.UUID) -> Optional[User]:
        result = await self.session.execute(select(UserModel).where(UserModel.id == id))
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None
    
    async def get_by_username(self, username: str) -> Optional[User]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.username == username)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None
    
    async def create(self, user: User) -> User:
        model = UserModel(
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password,
        )

        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)

        return model
    
    async def update(self, user: User) -> Optional[User]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user.id)
        )
        model = result.scalar_one_or_none()

        if not model:
            return None

        model.username = user.username
        model.email = user.email
        model.hashed_password = user.hashed_password

        await self.session.commit()
        await self.session.refresh(model)

        return model
  
    async def delete(self, id: uuid.UUID) -> bool:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == id)
        )
        model = result.scalar_one_or_none()

        if not model:
            return False

        await self.session.delete(model)
        await self.session.commit()
        return True