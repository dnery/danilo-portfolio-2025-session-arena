import os
from functools import lru_cache
from pydantic import Field, RedisDsn, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class DevSettings(BaseSettings):
    # not strictly necessary since we explicitly set env_file in the compose file
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    # the following would allow setting ENV directly in the shell environment
    # env: str = Field(default_factor=lambda: os.getenv("ENV", "dev"))
    env: str = "dev"
    debug: bool = True
    # database creds
    database_user: str = "arena"
    database_pass: str = "arena"
    database_host: str = "db"
    database_port: str = "5432"
    # database dsn
    database_url: PostgresDsn  # Required, but not defined here
    # redis creds
    redis_host: str = "redis"
    redis_port: str = "6379"
    # redis dsn
    database_url: PostgresDsn = f"postgresql+asyncpg://{database_user}:{database_pass}@{database_host}:{database_port}/arena_dev"
    # admin "secret"
    admin_user: str = "admin"
    admin_pass: str = "youcantseeme"
    # posthog config
    posthog_api_key: str = "blank"
    posthog_project: str = "blank"


class TestSettings(DevSettings):
    env: str = "test"
    debug: bool = True
    database_url: PostgresDsn = f"postgresql+asyncpg://{database_user}:{database_pass}@{database_host}:{database_port}/arena_test"


class ProdSettings(DevSettings):
    env: str = "prod"
    debug: bool = False
    database_url: PostgresDsn = f"postgresql+asyncpg://{database_user}:{database_pass}@{database_host}:{database_port}/arena"


@lru_cache
def get_settings() -> BaseSettings:
    defaults = DevSettings()
    env_name = defaults.env.lower()
    return {
            "dev": defaults,
            "test": TestSettings(),
            "prod": ProdSettings(),
            }


settings = get_settings()
