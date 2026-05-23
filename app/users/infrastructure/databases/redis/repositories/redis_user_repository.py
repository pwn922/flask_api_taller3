import uuid
from typing import List, Optional

from app.users.domain.user import User, UserRepository
from app.common.cache.redis_cache import RedisCache
from app.users.infrastructure.databases.postgresql.repositories.postgresql_user_repository import (
    PostgreSQLUserRepository,
)


class CachedUserRepository(UserRepository):
    CACHE_KEY_PREFIX = "user:"
    CACHE_ALL_KEY = "users:all"

    def __init__(self, pg_repository: PostgreSQLUserRepository, cache: RedisCache):
        self.pg_repository = pg_repository
        self.cache = cache

    def _to_dict(self, user: User) -> dict:
        return {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "hashed_password": user.hashed_password,
        }

    def _to_user(self, data: dict) -> User:
        return User(
            id=uuid.UUID(data["id"]),
            username=data["username"],
            email=data["email"],
            hashed_password=data.get("hashed_password"),
        )

    def _cache_key_by_id(self, id: uuid.UUID) -> str:
        return f"{self.CACHE_KEY_PREFIX}{id}"

    def _cache_key_by_email(self, email: str) -> str:
        return f"{self.CACHE_KEY_PREFIX}email:{email}"

    def _cache_key_by_username(self, username: str) -> str:
        return f"{self.CACHE_KEY_PREFIX}username:{username}"

    async def get_all(self) -> List[User]:
        cached = await self.cache.get(self.CACHE_ALL_KEY)
        if cached:
            return [self._to_user(u) for u in cached]

        users = await self.pg_repository.get_all()
        await self.cache.set(self.CACHE_ALL_KEY, [self._to_dict(u) for u in users])
        return users

    async def get_by_id(self, id: uuid.UUID) -> Optional[User]:
        cache_key = self._cache_key_by_id(id)
        cached = await self.cache.get(cache_key)
        if cached:
            print("get cache")
            return self._to_user(cached)

        user = await self.pg_repository.get_by_id(id)
        if user:
            print("set cache")
            await self.cache.set(cache_key, self._to_dict(user))

        print(user)
        return user

    async def get_by_email(self, email: str) -> Optional[User]:
        cache_key = self._cache_key_by_email(email)
        cached = await self.cache.get(cache_key)
        if cached:
            return self._to_user(cached)

        user = await self.pg_repository.get_by_email(email)
        if user:
            await self.cache.set(cache_key, self._to_dict(user))
        return user

    async def get_by_username(self, username: str) -> Optional[User]:
        cache_key = self._cache_key_by_username(username)
        cached = await self.cache.get(cache_key)
        if cached:
            return self._to_user(cached)

        user = await self.pg_repository.get_by_username(username)
        if user:
            await self.cache.set(cache_key, self._to_dict(user))
        return user

    async def create(self, user: User) -> User:
        created_user = await self.pg_repository.create(user)

        await self.cache.set(
            self._cache_key_by_id(created_user.id), self._to_dict(created_user)
        )
        await self.cache.set(
            self._cache_key_by_email(created_user.email), self._to_dict(created_user)
        )
        await self.cache.set(
            self._cache_key_by_username(created_user.username),
            self._to_dict(created_user),
        )
        await self.cache.delete(self.CACHE_ALL_KEY)

        return created_user

    async def update(self, user: User) -> Optional[User]:
        existing = await self.pg_repository.get_by_id(user.id)
        if not existing:
            return None

        old_email = existing.email
        old_username = existing.username

        updated_user = await self.pg_repository.update(user)

        await self.cache.set(
            self._cache_key_by_id(updated_user.id), self._to_dict(updated_user)
        )
        await self.cache.set(
            self._cache_key_by_email(updated_user.email), self._to_dict(updated_user)
        )
        await self.cache.set(
            self._cache_key_by_username(updated_user.username),
            self._to_dict(updated_user),
        )

        if old_email != updated_user.email:
            await self.cache.delete(self._cache_key_by_email(old_email))
        if old_username != updated_user.username:
            await self.cache.delete(self._cache_key_by_username(old_username))

        await self.cache.delete(self.CACHE_ALL_KEY)

        return updated_user

    async def delete(self, id: uuid.UUID) -> bool:
        existing = await self.pg_repository.get_by_id(id)
        if not existing:
            return False

        old_email = existing.email
        old_username = existing.username

        success = await self.pg_repository.delete(id)

        if success:
            await self.cache.delete(self._cache_key_by_id(id))
            await self.cache.delete(self._cache_key_by_email(old_email))
            await self.cache.delete(self._cache_key_by_username(old_username))
            await self.cache.delete(self.CACHE_ALL_KEY)

        return success
