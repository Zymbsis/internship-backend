from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, FastAPI, Request
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.config import settings
from app.exceptions.base import AppError


async def connect(app: FastAPI) -> None:
    engine: AsyncEngine = create_async_engine(settings.postgres.url, echo=settings.environment == "dev")
    sessionmaker = async_sessionmaker[AsyncSession](engine, expire_on_commit=False)

    async with engine.connect():
        pass

    app.state.pg_engine = engine
    app.state.pg_sessionmaker = sessionmaker


async def disconnect(app: FastAPI) -> None:
    pg_engine: AsyncEngine | None = getattr(app.state, "pg_engine", None)
    if pg_engine is not None:
        await pg_engine.dispose()


async def get_db(request: Request) -> AsyncGenerator[AsyncSession, None]:
    sessionmaker: async_sessionmaker[AsyncSession] | None = getattr(request.app.state, "pg_sessionmaker", None)
    if sessionmaker is None:
        raise AppError("PostgreSQL is not initialized")

    async with sessionmaker() as session:
        yield session


DbSessionDep = Annotated[AsyncSession, Depends(get_db)]
