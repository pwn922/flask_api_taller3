import uuid

from app.users.application.exceptions.user_already_exists_error import UserAlreadyExistsError
from app.users.domain.user import User, UserRepository


class CreateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, username: str, email: str, hashed_password: str) -> User:
        existing_user = await self.user_repository.get_by_email(email)
        if existing_user:
            raise UserAlreadyExistsError(f"The email '{email}' is already in use.")

        existing_user_by_username = await self.user_repository.get_by_username(username)
        if existing_user_by_username:
            raise UserAlreadyExistsError(f"The username '{username}' is already in use.")
        
        user = User(
            id=None,
            username=username,
            email=email,
            hashed_password=hashed_password,
        )
        
        return await self.user_repository.create(user)