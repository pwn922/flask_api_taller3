from abc import ABC, abstractmethod


class PasswordHasher(ABC):
    @staticmethod
    @abstractmethod
    def hash(password: str) -> str:
        pass

    @staticmethod
    @abstractmethod
    def verify_password(password: str, hash: str) -> bool:
        pass
