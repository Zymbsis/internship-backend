from fastapi import Request
from fastapi.responses import JSONResponse
from starlette import status

from app.exceptions.base import AppError, ForbiddenError, NotFoundError


async def handle_not_found(_request: Request, exc: Exception) -> JSONResponse:
    if not isinstance(exc, NotFoundError):
        raise exc

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.message},
    )


async def handle_forbidden(_request: Request, exc: Exception) -> JSONResponse:
    if not isinstance(exc, ForbiddenError):
        raise exc

    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": exc.message},
    )


async def handle_app_error(_request: Request, exc: Exception) -> JSONResponse:
    if not isinstance(exc, AppError):
        raise exc

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": exc.message},
    )
