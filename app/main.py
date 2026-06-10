import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.core.logging import setup_logging
from app.db import postgres, redis
from app.exceptions.base import AppError, ConflictError, ForbiddenError, NotFoundError
from app.exceptions.handlers import handle_app_error, handle_conflict, handle_forbidden, handle_not_found
from app.routers.api import api_router

logger = logging.getLogger(__name__)

setup_logging(settings.environment)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger.info("Starting application")
    await postgres.connect(app)
    await redis.initialize(app)

    yield

    await redis.shutdown(app)
    await postgres.disconnect(app)
    logger.info("Application stopped")


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
app.add_exception_handler(ConflictError, handle_conflict)
app.add_exception_handler(ForbiddenError, handle_forbidden)
app.add_exception_handler(AppError, handle_app_error)
