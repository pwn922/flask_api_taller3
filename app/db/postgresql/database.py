from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from app.config import ActiveConfig


DB_URL = f"postgresql+asyncpg://{ActiveConfig.DB_USER}:{ActiveConfig.DB_PASSWORD}@{ActiveConfig.DB_HOST}:{ActiveConfig.DB_PORT}/{ActiveConfig.DB_NAME}"
engine = create_async_engine(DB_URL, echo=ActiveConfig.DEBUG, pool_pre_ping=True)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

Base = declarative_base()
