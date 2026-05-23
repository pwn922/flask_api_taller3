from app.common.utils.password_hasher import PasswordHasher


class GeneratePasswordUseCase:
    def __init__(self, password_hasher: PasswordHasher):
        self.password_hasher = password_hasher

    def execute(self, password: str) -> str:
        return self.password_hasher.hash(password)
