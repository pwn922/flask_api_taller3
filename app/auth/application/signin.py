from app.users.domain.user import User, UserRepository

# llamar password hasher para comprobar credenciales
class SignInUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, email: str, password: str) -> User:
        user = await self.user_repository.get_by_email(email)

        if not user:
            raise ValueError("Incorrect credentials.")
       
        return user
