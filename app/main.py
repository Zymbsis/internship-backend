from fastapi import FastAPI

from app.exceptions.base import AppError
from app.exceptions.handlers import app_error_handler
from app.routers.api import api_router

app = FastAPI()

app.include_router(api_router)
app.add_exception_handler(AppError, app_error_handler)
