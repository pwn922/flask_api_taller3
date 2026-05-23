from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.application.signin import SignInUseCase
from app.auth.application.signup import SignUpUseCase
from app.db. import get_db
from app.users.infrastructure.databases.postgresql.repositories.postgresql_user_repository import (
    PostgreSQLUserRepository,
)

# TODO: Mejorar codigo de estados
# TODO: Investigar DTO en Python

router = APIRouter(prefix="/v1/auth")


from pydantic import BaseModel


class SignInRequest(BaseModel):
    email: str
    password: str


@router.post("/signin")
async def signIn(data: SignInRequest, db: AsyncSession = Depends(get_db)):
    try:
        repository = PostgreSQLUserRepository(db)
        signin_usecase = SignInUseCase(repository)
        await signin_usecase.execute(data.email, data.password)
        return {"id": data.email, "name": data.password}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/signup")
async def signUp(name: str, email: str, db: AsyncSession = Depends(get_db)):
    repository = PostgreSQLUserRepository(db)
    signup_usecase = SignUpUseCase(repository)
    try:
        user = await signup_usecase.execute(name, email)
        return {"id": str(user.id), "name": user.name, "email": user.email}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
