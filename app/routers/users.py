from uuid import UUID

from fastapi import APIRouter, status

from app.schemas.common import FilterParamsDep
from app.schemas.user import UserCreate, UserDetailResponse, UsersListResponse, UserUpdateRequest
from app.services.user_service import UserServiceDep

router = APIRouter()


@router.get("/", response_model=UsersListResponse)
async def get_users_list(filters: FilterParamsDep, user_service: UserServiceDep) -> UsersListResponse:
    return await user_service.get_users(filters)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserDetailResponse)
async def create_user(payload: UserCreate, user_service: UserServiceDep) -> UserDetailResponse:
    return await user_service.create_user(payload)


@router.get("/{user_id}", response_model=UserDetailResponse)
async def get_user_detail(user_id: UUID, user_service: UserServiceDep) -> UserDetailResponse:
    return await user_service.get_user_by_id(user_id)


@router.patch("/{user_id}", response_model=UserDetailResponse)
async def update_user(user_id: UUID, payload: UserUpdateRequest, user_service: UserServiceDep) -> UserDetailResponse:
    return await user_service.update_user(user_id, payload)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: UUID, user_service: UserServiceDep) -> None:
    await user_service.delete_user(user_id)
