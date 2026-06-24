import uuid
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field, StringConstraints

from app.core.constants import (
    EMAIL_MAX_LENGTH,
    FIRST_NAME_MAX_LENGTH,
    LAST_NAME_MAX_LENGTH,
    PASSWORD_MAX_LENGTH,
    PASSWORD_MIN_LENGTH,
)


class UserCredentials(BaseModel):
    email: EmailStr = Field(max_length=EMAIL_MAX_LENGTH)
    password: str = Field(min_length=PASSWORD_MIN_LENGTH, max_length=PASSWORD_MAX_LENGTH)


class UserCreate(UserCredentials):
    first_name: Annotated[str | None, StringConstraints(strip_whitespace=True, max_length=FIRST_NAME_MAX_LENGTH)] = None
    last_name: Annotated[str | None, StringConstraints(strip_whitespace=True, max_length=LAST_NAME_MAX_LENGTH)] = None


class User(BaseModel, from_attributes=True):
    id: uuid.UUID
    email: EmailStr = Field(max_length=EMAIL_MAX_LENGTH)
    first_name: str | None = Field(None, max_length=FIRST_NAME_MAX_LENGTH)
    last_name: str | None = Field(None, max_length=LAST_NAME_MAX_LENGTH)
    is_active: bool


class UserDetailResponse(User):
    pass


class UsersListResponse(BaseModel):
    users: list[UserDetailResponse]
    total: int = Field(ge=0)


class UserUpdateRequest(BaseModel):
    first_name: Annotated[str | None, StringConstraints(strip_whitespace=True, max_length=FIRST_NAME_MAX_LENGTH)] = None
    last_name: Annotated[str | None, StringConstraints(strip_whitespace=True, max_length=LAST_NAME_MAX_LENGTH)] = None
