from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.requests import HTTPConnection
from redis import asyncio as aioredis
from redis.asyncio import Redis

from app.config import settings
from app.exceptions.base import AppError


async def initialize(app: FastAPI) -> None:
    redis_client = aioredis.from_url(settings.redis.url, decode_responses=True)
    await redis_client.ping()

    app.state.redis = redis_client


async def shutdown(app: FastAPI) -> None:
    redis_client: Redis | None = getattr(app.state, "redis", None)
    if redis_client is not None:
        await redis_client.aclose()


def get_redis(conn: HTTPConnection) -> Redis:
    redis_client: Redis | None = getattr(conn.app.state, "redis", None)
    if redis_client is None:
        raise AppError("Redis is not initialized")
    return redis_client


RedisDep = Annotated[Redis, Depends(get_redis)]
