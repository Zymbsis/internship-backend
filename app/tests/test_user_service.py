from datetime import UTC, datetime
from typing import cast
from unittest.mock import AsyncMock, create_autospec, patch
from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.exceptions.base import ConflictError, NotFoundError
from app.models import User as UserModel
from app.repositories.user_repository import UserRepository
from app.schemas.common import FilterParams
from app.schemas.user import UserCreate, UserDetailResponse, UserUpdateRequest
from app.services.user_service import UserService

TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "password1"
TEST_FIRST_NAME = "Jane"
TEST_LAST_NAME = "Doe"
UPDATED_FIRST_NAME = "Joe"
UPDATED_LAST_NAME = "Smith"


def make_user(**kwargs: object) -> UserModel:
    defaults: dict[str, object] = {
        "id": uuid4(),
        "email": TEST_EMAIL,
        "hashed_password": "hashed",
        "first_name": TEST_FIRST_NAME,
        "last_name": TEST_LAST_NAME,
        "is_active": True,
        "created_at": datetime.now(UTC),
        "updated_at": datetime.now(UTC),
    }
    defaults.update(kwargs)
    return UserModel(**defaults)


@pytest.fixture
def user_repository() -> AsyncMock:
    return cast(AsyncMock, create_autospec(UserRepository, instance=True))


@pytest.fixture
def session() -> AsyncMock:
    return cast(AsyncMock, create_autospec(AsyncSession, instance=True))


@pytest.fixture
def user_service(user_repository: AsyncMock, session: AsyncMock) -> UserService:
    return UserService(
        cast(UserRepository, user_repository),
        cast(AsyncSession, session),
    )


async def test_get_users_returns_paginated_users(
    user_service: UserService,
    user_repository: AsyncMock,
) -> None:
    user = make_user()
    user_repository.get_many.return_value = ([user], 1)

    result = await user_service.get_users(FilterParams(page=1, limit=10))

    user_repository.get_many.assert_awaited_once_with(0, 10)
    assert result.total == 1
    assert result.users == [UserDetailResponse.model_validate(user)]


async def test_get_user_by_id_returns_user(
    user_service: UserService,
    user_repository: AsyncMock,
) -> None:
    user = make_user()
    user_repository.get_one_by_id.return_value = user

    result = await user_service.get_user_by_id(user.id)

    user_repository.get_one_by_id.assert_awaited_once_with(user.id)
    assert result == UserDetailResponse.model_validate(user)


async def test_get_user_by_id_raises_not_found(
    user_service: UserService,
    user_repository: AsyncMock,
) -> None:
    user_id = uuid4()
    user_repository.get_one_by_id.return_value = None

    with pytest.raises(NotFoundError, match="User not found"):
        await user_service.get_user_by_id(user_id)


async def test_create_user_returns_user_and_commits(
    user_service: UserService,
    user_repository: AsyncMock,
    session: AsyncMock,
) -> None:
    user = make_user()
    user_repository.get_one_by_email.return_value = None
    user_repository.create.return_value = user
    payload = UserCreate(
        email=TEST_EMAIL,
        password=TEST_PASSWORD,
        first_name=TEST_FIRST_NAME,
        last_name=TEST_LAST_NAME,
    )

    with patch("app.services.user_service.get_password_hash", return_value="hashed"):
        result = await user_service.create_user(payload)

    user_repository.get_one_by_email.assert_awaited_once_with(payload.email)
    user_repository.create.assert_awaited_once()
    session.commit.assert_awaited_once()
    assert result == UserDetailResponse.model_validate(user)


async def test_create_user_raises_conflict_when_email_exists(
    user_service: UserService,
    user_repository: AsyncMock,
    session: AsyncMock,
) -> None:
    existing = make_user()
    user_repository.get_one_by_email.return_value = existing
    payload = UserCreate(
        email=TEST_EMAIL,
        password=TEST_PASSWORD,
        first_name=TEST_FIRST_NAME,
        last_name=TEST_LAST_NAME,
    )

    with pytest.raises(ConflictError, match="User with this email already exists"):
        await user_service.create_user(payload)

    user_repository.create.assert_not_awaited()
    session.commit.assert_not_awaited()


async def test_update_user_updates_fields_and_commits(
    user_service: UserService,
    user_repository: AsyncMock,
    session: AsyncMock,
) -> None:
    user = make_user()
    user_repository.get_one_by_id.return_value = user
    user_repository.update.return_value = user
    payload = UserUpdateRequest(first_name=UPDATED_FIRST_NAME, last_name=UPDATED_LAST_NAME)

    result = await user_service.update_user(user.id, payload)

    assert user.first_name == UPDATED_FIRST_NAME
    assert user.last_name == UPDATED_LAST_NAME
    user_repository.update.assert_awaited_once_with(user)
    session.commit.assert_awaited_once()
    assert result == UserDetailResponse.model_validate(user)


async def test_update_user_raises_not_found(
    user_service: UserService,
    user_repository: AsyncMock,
    session: AsyncMock,
) -> None:
    user_id = uuid4()
    user_repository.get_one_by_id.return_value = None
    payload = UserUpdateRequest(first_name=UPDATED_FIRST_NAME, last_name=None)

    with pytest.raises(NotFoundError, match="User not found"):
        await user_service.update_user(user_id, payload)

    user_repository.update.assert_not_awaited()
    session.commit.assert_not_awaited()


async def test_delete_user_deletes_and_commits(
    user_service: UserService,
    user_repository: AsyncMock,
    session: AsyncMock,
) -> None:
    user = make_user()
    user_repository.get_one_by_id.return_value = user

    await user_service.delete_user(user.id)

    user_repository.delete.assert_awaited_once_with(user)
    session.commit.assert_awaited_once()


async def test_delete_user_raises_not_found(
    user_service: UserService,
    user_repository: AsyncMock,
    session: AsyncMock,
) -> None:
    user_id = uuid4()
    user_repository.get_one_by_id.return_value = None

    with pytest.raises(NotFoundError, match="User not found"):
        await user_service.delete_user(user_id)

    user_repository.delete.assert_not_awaited()
    session.commit.assert_not_awaited()
