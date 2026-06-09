from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db import postgres, redis
from app.exceptions.base import AppError, ForbiddenError, NotFoundError
from app.exceptions.handlers import handle_app_error, handle_forbidden, handle_not_found
from app.routers.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    await postgres.connect(app)
    await redis.initialize(app)

    yield

    await redis.shutdown(app)
    await postgres.disconnect(app)


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(api_router)
app.add_exception_handler(NotFoundError, handle_not_found)
app.add_exception_handler(ForbiddenError, handle_forbidden)
app.add_exception_handler(AppError, handle_app_error)
