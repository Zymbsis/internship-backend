from fastapi import APIRouter

from app.routers import health, users

api_router = APIRouter(prefix="/api")

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
