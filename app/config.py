import os
from pydantic import RedisDsn, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    # not strictly necessary since we explicitly set env_file in the compose file
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    # the following would conveniently force validation of a shell-overridable variable
    # var: str = Field(default_factory=lambda: os.getenv("VAR", "value"))
    debug: bool = True
    # database
    database_url: PostgresDsn = "postgresql+asyncpg://arena:arena@db:5432/arena"
    # redis
    redis_url: RedisDsn = "redis://redis:6379/0"
    # "admin"
    admin_user: str = "admin"
    admin_pass: str = "youcantseeme"
    # posthog config
    posthog_api_key: str = "blank"
    posthog_project: str = "blank"


settings = AppSettings()
