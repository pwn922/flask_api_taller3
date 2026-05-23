from app.auth.domain.ports.token_manager import TokenManager


class CreateAccessTokenUseCase:
    def __init__(self, token_manager: TokenManager):
        self.token_manager = token_manager

    def execute(self, user_id: str) -> str:
        return self.token_manager.create_access_token(user_id)
