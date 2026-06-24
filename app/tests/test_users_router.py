from collections.abc import Iterator
from typing import cast
from unittest.mock import AsyncMock, create_autospec, patch
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient
from httpx2 import Response
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)

from app.exceptions.base import ConflictError, NotFoundError
from app.main import app
from app.schemas.user import UserCreate, UserDetailResponse, UsersListResponse, UserUpdateRequest
from app.services.user_service import UserService

TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "password1"
TEST_FIRST_NAME = "Jane"
TEST_LAST_NAME = "Doe"
UPDATED_FIRST_NAME = "Joe"
UPDATED_LAST_NAME = "Smith"


def make_user_detail(
    *,
    user_id: UUID | None = None,
    email: str = TEST_EMAIL,
    first_name: str | None = TEST_FIRST_NAME,
    last_name: str | None = TEST_LAST_NAME,
    is_active: bool = True,
) -> UserDetailResponse:
    return UserDetailResponse(
        id=user_id or uuid4(),
        email=email,
        first_name=first_name,
        last_name=last_name,
        is_active=is_active,
    )


@pytest.fixture
def user_service_mock() -> AsyncMock:
    return cast(AsyncMock, create_autospec(UserService, instance=True))


@pytest.fixture
def users_client(user_service_mock: AsyncMock) -> Iterator[TestClient]:
    app.dependency_overrides[UserService] = lambda: user_service_mock
    with (
        patch("app.db.postgres.connect", new=AsyncMock()),
        patch("app.db.redis.initialize", new=AsyncMock()),
        TestClient(app) as test_client,
    ):
        yield test_client
    app.dependency_overrides.clear()


def test_get_users_list(users_client: TestClient, user_service_mock: AsyncMock) -> None:
    user = make_user_detail()
    user_service_mock.get_users = AsyncMock(return_value=UsersListResponse(users=[user], total=1))

    response: Response = users_client.get("/api/users/")

    assert response.status_code == HTTP_200_OK
    assert UsersListResponse.model_validate(response.json()) == UsersListResponse(users=[user], total=1)


def test_get_user_detail(users_client: TestClient, user_service_mock: AsyncMock) -> None:
    user = make_user_detail()
    user_service_mock.get_user_by_id = AsyncMock(return_value=user)

    response: Response = users_client.get(f"/api/users/{user.id}")

    assert response.status_code == HTTP_200_OK
    assert UserDetailResponse.model_validate(response.json()) == user


def test_get_user_detail_not_found(users_client: TestClient, user_service_mock: AsyncMock) -> None:
    user_id = uuid4()
    user_service_mock.get_user_by_id = AsyncMock(side_effect=NotFoundError("User not found"))

    response: Response = users_client.get(f"/api/users/{user_id}")

    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_create_user(users_client: TestClient, user_service_mock: AsyncMock) -> None:
    user = make_user_detail()
    user_service_mock.create_user = AsyncMock(return_value=user)
    payload = UserCreate(
        email=TEST_EMAIL,
        password=TEST_PASSWORD,
        first_name=TEST_FIRST_NAME,
        last_name=TEST_LAST_NAME,
    )

    response: Response = users_client.post("/api/users/", json=payload.model_dump())

    assert response.status_code == HTTP_201_CREATED
    assert UserDetailResponse.model_validate(response.json()) == user


def test_create_user_conflict(users_client: TestClient, user_service_mock: AsyncMock) -> None:
    user_service_mock.create_user = AsyncMock(side_effect=ConflictError("User with this email already exists"))
    payload = UserCreate(
        email=TEST_EMAIL,
        password=TEST_PASSWORD,
        first_name=TEST_FIRST_NAME,
        last_name=TEST_LAST_NAME,
    )

    response: Response = users_client.post("/api/users/", json=payload.model_dump())

    assert response.status_code == HTTP_409_CONFLICT
    assert response.json() == {"detail": "User with this email already exists"}


def test_update_user(users_client: TestClient, user_service_mock: AsyncMock) -> None:
    user = make_user_detail(first_name=UPDATED_FIRST_NAME, last_name=UPDATED_LAST_NAME)
    user_service_mock.update_user = AsyncMock(return_value=user)
    payload = UserUpdateRequest(first_name=UPDATED_FIRST_NAME, last_name=UPDATED_LAST_NAME)

    response: Response = users_client.patch(f"/api/users/{user.id}", json=payload.model_dump())

    assert response.status_code == HTTP_200_OK
    assert UserDetailResponse.model_validate(response.json()) == user


def test_update_user_not_found(users_client: TestClient, user_service_mock: AsyncMock) -> None:
    user_id = uuid4()
    user_service_mock.update_user = AsyncMock(side_effect=NotFoundError("User not found"))
    payload = UserUpdateRequest(first_name=UPDATED_FIRST_NAME)

    response: Response = users_client.patch(f"/api/users/{user_id}", json=payload.model_dump())

    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_delete_user(users_client: TestClient, user_service_mock: AsyncMock) -> None:
    user_id = uuid4()
    user_service_mock.delete_user = AsyncMock(return_value=None)

    response: Response = users_client.delete(f"/api/users/{user_id}")

    assert response.status_code == HTTP_204_NO_CONTENT
    assert response.content == b""


def test_delete_user_not_found(users_client: TestClient, user_service_mock: AsyncMock) -> None:
    user_id = uuid4()
    user_service_mock.delete_user = AsyncMock(side_effect=NotFoundError("User not found"))

    response: Response = users_client.delete(f"/api/users/{user_id}")

    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "User not found"}
