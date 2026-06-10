from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy import func, select

from app.db.postgres import DbSessionDep
from app.models import User


class UserRepository:
    def __init__(self, session: DbSessionDep) -> None:
        self._session = session

    async def get_one_by_id(self, user_id: UUID) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_one_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_many(self, offset: int, limit: int) -> tuple[list[User], int]:
        users_stmt = select(User).order_by(User.created_at).offset(offset).limit(limit)
        users = list(await self._session.scalars(users_stmt))

        total_stmt = select(func.count(User.id)).select_from(User)
        total_results = await self._session.execute(total_stmt)
        total = total_results.scalar_one()

        return users, total or 0

    async def create(self, user: User) -> User:
        self._session.add(user)
        await self._session.flush()
        await self._session.refresh(user)
        return user

    async def update(self, user: User) -> User:
        await self._session.flush()
        await self._session.refresh(user)
        return user

    async def delete(self, user: User) -> None:
        await self._session.delete(user)


UserRepositoryDep = Annotated[UserRepository, Depends()]
