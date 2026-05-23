from typing import List

from app.users.domain.user import User, UserRepository


class GetUsersUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self) -> List[User]:
        return await self.user_repository.get_all()