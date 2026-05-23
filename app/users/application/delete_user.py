import uuid
from typing import Optional

from app.users.domain.user import User, UserRepository


class DeleteUserByIdUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, user_id: uuid.UUID) -> None:
        return await self.user_repository.delete(user_id)
