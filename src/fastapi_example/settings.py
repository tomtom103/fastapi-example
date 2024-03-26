from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Base(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )


class RedisSettings(Base):
    REDIS_HOST: str = "0.0.0.0"
    REDIS_PORT: int = 2679


class APISettings(Base):
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_NAME: str = "FastAPI Example"

    DEBUG: bool = True


class Settings(APISettings, RedisSettings): ...


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


@lru_cache(maxsize=1)
def get_api_settings() -> APISettings:
    return APISettings()


@lru_cache(maxsize=1)
def get_redis_settings() -> RedisSettings:
    return RedisSettings()
