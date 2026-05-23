from app.users.domain.user import User, UserRepository


class SignUpUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, name: str, email: str) -> User:
        existing = await self.user_repository.get_by_email(email)
        if existing:
            raise ValueError("Email already registered")

        user = User(id="", name=name, email=email)
        await self.user_repository.create(user)
        return user
