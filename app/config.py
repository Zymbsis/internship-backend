from functools import lru_cache
from typing import Annotated, Literal

from fastapi import Depends
from pydantic import BaseModel, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseModel):
    user: str = "postgres"
    password: str = "password"
    db: str = "postgres"
    host: str = "localhost"
    port: int = 5432

    @computed_field
    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class RedisSettings(BaseModel):
    host: str = "localhost"
    port: int = 6379

    @computed_field
    @property
    def url(self) -> str:
        return f"redis://{self.host}:{self.port}"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_nested_delimiter="__")

    environment: Literal["dev", "prod"] = "dev"
    cors_origins: list[str] = []

    postgres: PostgresSettings
    redis: RedisSettings


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
SettingsDep = Annotated[Settings, Depends(get_settings)]
