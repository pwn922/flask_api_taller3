import uuid
from typing import Optional

from app.users.domain.user import User, UserRepository


class GetUserByIdUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, user_id: uuid.UUID) -> Optional[User]:
        return await self.user_repository.get_by_id(user_id)
