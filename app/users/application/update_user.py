import uuid
from typing import Optional

from app.users.domain.user import User, UserRepository


class UpdateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(
        self, user_id: uuid.UUID, username: str, email: str
    ) -> Optional[User]:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            return None
        user.username = username
        user.email = email
        await self.user_repository.update(user)
        return user
