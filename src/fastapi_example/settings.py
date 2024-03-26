from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Base(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )


class APISettings(Base):
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_NAME: str = "FastAPI Example"

    DEBUG: bool = True


class Settings(APISettings): ...


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


@lru_cache(maxsize=1)
def get_api_settings() -> APISettings:
    return APISettings()
