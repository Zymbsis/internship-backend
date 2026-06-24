from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.constants import EMAIL_MAX_LENGTH, FIRST_NAME_MAX_LENGTH, HASHED_PASSWORD_MAX_LENGTH, LAST_NAME_MAX_LENGTH
from app.models.base import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class User(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(EMAIL_MAX_LENGTH), unique=True, index=True)
    hashed_password: Mapped[str | None] = mapped_column(String(HASHED_PASSWORD_MAX_LENGTH))
    first_name: Mapped[str | None] = mapped_column(String(FIRST_NAME_MAX_LENGTH))
    last_name: Mapped[str | None] = mapped_column(String(LAST_NAME_MAX_LENGTH))
    is_active: Mapped[bool] = mapped_column(default=True)
