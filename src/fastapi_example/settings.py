from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Base(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )


class RedisSettings(Base):
    REDIS_HOST: str = "0.0.0.0"
    REDIS_PORT: int = 2679
    REDIS_TIMEOUT: float = 0.1


class APISettings(Base):
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_NAME: str = "FastAPI Boilerplate"

    DEBUG: bool = True


class LoggingSettings(Base):
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(message)s"
    LOG_DATE_FORMAT: str = "%Y-%m-%dT%H:%M:%S%z"


class Settings(APISettings, RedisSettings, LoggingSettings):
    """Combined view of all settings"""


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


@lru_cache(maxsize=1)
def get_api_settings() -> APISettings:
    return APISettings()


@lru_cache(maxsize=1)
def get_redis_settings() -> RedisSettings:
    return RedisSettings()


@lru_cache(maxsize=1)
def get_logging_settings() -> LoggingSettings:
    return LoggingSettings()
