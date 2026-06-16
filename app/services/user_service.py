import logging
from typing import Annotated
from uuid import UUID

from fastapi import Depends

from app.exceptions.base import ConflictError, NotFoundError
from app.models import User as UserModel
from app.repositories.user_repository import UserRepositoryDep
from app.schemas.common import FilterParams
from app.schemas.user import UserCreate, UserDetailResponse, UsersListResponse, UserUpdateRequest
from app.utils.password import get_password_hash

logger = logging.getLogger(__name__)


class UserService:
    def __init__(
        self,
        user_repository: UserRepositoryDep,
    ) -> None:
        self._user_repository = user_repository

    async def get_users(self, filters: FilterParams) -> UsersListResponse:
        offset, limit = (filters.page - 1) * filters.limit, filters.limit
        users, total = await self._user_repository.get_many(offset, limit)

        return UsersListResponse(users=[UserDetailResponse.model_validate(user) for user in users], total=total)

    async def get_user_by_id(self, user_id: UUID) -> UserDetailResponse:
        user = await self._user_repository.get_one_by_id(user_id)
        if user is None:
            raise NotFoundError("User not found")

        return UserDetailResponse.model_validate(user)

    async def create_user(self, data: UserCreate) -> UserDetailResponse:
        existing = await self._user_repository.get_one_by_email(data.email)
        if existing is not None:
            raise ConflictError("User with this email already exists")

        user = UserModel(
            email=data.email,
            hashed_password=get_password_hash(data.password),
            first_name=data.first_name,
            last_name=data.last_name,
        )
        created = await self._user_repository.create(user)
        await self._user_repository.commit()

        detail = f"User created: user_id={created.id} email={created.email}"
        logger.info(detail)

        return UserDetailResponse.model_validate(created)

    async def update_user(self, user_id: UUID, payload: UserUpdateRequest) -> UserDetailResponse:
        existing = await self._user_repository.get_one_by_id(user_id)
        if existing is None:
            raise NotFoundError("User not found")

        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(existing, field, value)
        updated = await self._user_repository.update(existing)
        await self._user_repository.commit()

        detail = f"User updated: user_id={updated.id}"
        logger.info(detail)

        return UserDetailResponse.model_validate(updated)

    async def delete_user(self, user_id: UUID) -> None:
        existing = await self._user_repository.get_one_by_id(user_id)
        if existing is None:
            raise NotFoundError("User not found")

        await self._user_repository.delete(existing)
        await self._user_repository.commit()

        detail = f"User deleted: user_id={user_id}"
        logger.info(detail)


UserServiceDep = Annotated[UserService, Depends()]
