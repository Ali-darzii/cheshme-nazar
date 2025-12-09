from typing import AsyncGenerator
from contextlib import asynccontextmanager

from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from src.config import setting

async_engine = create_async_engine(setting.POSTGRE_DB, echo=setting.DEBUG, future=True)
AsyncSessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)


async def init_postdb() -> None:
    """
    Create all tables on startup.
    Use in FastAPI lifespan or startup event.
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_postdb() -> AsyncGenerator[AsyncSession, None]:
    """
    Async session dependency for FastAPI.
    Use with Depends(get_postdb)
    """
    async with AsyncSessionLocal() as session:
        yield session

@asynccontextmanager
async def get_postdb_cm() -> AsyncGenerator[AsyncSession, None]:
    """
    Async context manager for scripts or batch jobs.
    """
    async with AsyncSessionLocal() as session:
        yield session
