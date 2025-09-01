import os
from functools import lru_cache, cached_property
from pydantic import Field, RedisDsn, PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DevSettings(BaseSettings):
    # not strictly necessary since we explicitly set env_file in the compose file
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    # the following would conveniently force validation of the ENV variable
    #env: str = Field(default_factory=lambda: os.getenv("ENV", "dev"))
    env: str = "dev"
    debug: bool = True
    # database dsn
    database_url: PostgresDsn = "postgresql+asyncpg://arena:arena@db:5432/arena_dev"
    # redis dsn
    redis_url: RedisDsn = "redis://redis:6379/0"
    # admin "secret"
    admin_user: str = "admin"
    admin_pass: str = "youcantseeme"
    # posthog config
    posthog_api_key: str = "blank"
    posthog_project: str = "blank"


class TestSettings(DevSettings):
    env: str = "test"
    debug: bool = True
    database_url: PostgresDsn = "postgresql+asyncpg://arena:arena@db:5432/arena_test"


class ProdSettings(DevSettings):
    env: str = "prod"
    debug: bool = False
    database_url: PostgresDsn = "postgresql+asyncpg://arena:arena@db:5432/arena"


@lru_cache
def get_settings() -> BaseSettings:
    env_name = os.getenv("ENV", "dev").lower()
    return {
            "dev": DevSettings(),
            "test": TestSettings(),
            "prod": ProdSettings(),
            }[env_name]


settings = get_settings()
