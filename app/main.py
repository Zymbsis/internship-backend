from fastapi import FastAPI

from app.exceptions.base import AppError, ForbiddenError, NotFoundError
from app.exceptions.handlers import handle_app_error, handle_forbidden, handle_not_found
from app.routers.api import api_router

app = FastAPI()

app.include_router(api_router)
app.add_exception_handler(NotFoundError, handle_not_found)
app.add_exception_handler(ForbiddenError, handle_forbidden)
app.add_exception_handler(AppError, handle_app_error)
