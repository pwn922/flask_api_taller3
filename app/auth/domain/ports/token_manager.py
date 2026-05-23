from abc import ABC, abstractmethod

class TokenManager(ABC):

    @abstractmethod
    def create_access_token(self, user_id: str) -> str:
        pass

    @abstractmethod
    def create_refresh_token(self, user_id: str) -> str:
        pass

    @abstractmethod
    def verify_token(token: str) -> dict:
        pass