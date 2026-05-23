from __future__ import annotations

import uuid

from app.users.application.exceptions.user_already_exists_error import (
    UserAlreadyExistsError,
)
from fastapi import APIRouter, Depends, HTTPException
from fastapi import status

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.postgresql.database import get_db
from app.users.application import CreateUserUseCase, GetUserByIdUseCase, GetUsersUseCase

from app.users.application.delete_user import DeleteUserByIdUseCase
from app.users.application.update_user import UpdateUserUseCase
from app.common.dependencies import get_redis_cache
from app.common.cache.redis_cache import RedisCache
from app.users.infrastructure.databases.postgresql.repositories.postgresql_user_repository import (
    PostgreSQLUserRepository,
)
from app.users.infrastructure.databases.redis.repositories.redis_user_repository import (
    CachedUserRepository,
)

from app.common.utils.bcrypt_password_hasher import BcryptPasswordHasher

from pydantic import BaseModel


router = APIRouter(prefix="/v1/users")


@router.get("/{user_id}")
async def get_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    cache: RedisCache = Depends(get_redis_cache),
):
    pg_user_repository = PostgreSQLUserRepository(db)
    cache_user_repository = CachedUserRepository(pg_user_repository, cache)
    use_case = GetUserByIdUseCase(cache_user_repository)
    user = await use_case.execute(uuid.UUID(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": str(user.id), "username": user.username, "email": user.email}


@router.get("")
async def get_users(
    db: AsyncSession = Depends(get_db),
    cache: RedisCache = Depends(get_redis_cache),
):
    pg_user_repository = PostgreSQLUserRepository(db)
    cache_user_repository = CachedUserRepository(pg_user_repository, cache)
    use_case = GetUsersUseCase(cache_user_repository)
    users = await use_case.execute()
    return [{"id": str(u.id), "username": u.username, "email": u.email} for u in users]


class UserRequest(BaseModel):
    username: str
    email: str
    password: str


class UpdateUserRequest(BaseModel):
    username: str
    email: str


@router.post("")
async def create_user(
    data: UserRequest,
    db: AsyncSession = Depends(get_db),
    cache: RedisCache = Depends(get_redis_cache),
):
    if not data.username or not data.email or not data.password:
        raise HTTPException(
            status_code=400, detail="Username, email, and password are required"
        )

    pg_user_repository = PostgreSQLUserRepository(db)
    cache_user_repository = CachedUserRepository(pg_user_repository, cache)
    use_case = CreateUserUseCase(cache_user_repository)

    hashed_password = BcryptPasswordHasher.hash(password=data.password)

    try:
        user = await use_case.execute(data.username, data.email, hashed_password)
        return {"id": str(user.id), "username": user.username, "email": user.email}

    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{user_id}")
async def update_user(
    user_id: str,
    data: UpdateUserRequest,
    db: AsyncSession = Depends(get_db),
    cache: RedisCache = Depends(get_redis_cache),
):
    if not data.username or not data.email:
        raise HTTPException(status_code=400, detail="username and email required")

    pg_user_repository = PostgreSQLUserRepository(db)
    cache_user_repository = CachedUserRepository(pg_user_repository, cache)
    use_case = UpdateUserUseCase(cache_user_repository)
    user = await use_case.execute(uuid.UUID(user_id), data.username, data.email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"id": str(user.id), "username": user.username, "email": user.email}


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    cache: RedisCache = Depends(get_redis_cache),
):
    pg_user_repository = PostgreSQLUserRepository(db)
    cache_user_repository = CachedUserRepository(pg_user_repository, cache)
    use_case = DeleteUserByIdUseCase(cache_user_repository)

    success = await use_case.execute(uuid.UUID(user_id))

    if not success:
        raise HTTPException(status_code=404, detail="User not found")
