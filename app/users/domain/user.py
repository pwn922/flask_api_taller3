from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from typing import List, Optional


class User:
    def __init__(
        self,
        id: Optional[uuid.UUID],
        username: str,
        email: str,
        hashed_password: Optional[str] = None,
    ):
        self.id = id
        self.username = username
        self.email = email
        self.hashed_password = hashed_password

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"


class UserRepository(ABC):
    @abstractmethod
    async def get_all(self) -> List[User]:
        pass

    @abstractmethod
    async def get_by_id(self, id: uuid.UUID) -> Optional[User]:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[User]:
        pass

    @abstractmethod
    async def create(self, user: User) -> None:
        pass

    @abstractmethod
    async def update(self, user: User) -> None:
        pass

    @abstractmethod
    async def delete(self, id: uuid.UUID) -> None:
        pass
