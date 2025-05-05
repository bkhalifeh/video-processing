from pydantic_settings import BaseSettings, SettingsConfigDict

from fastapi import Depends
from typing import Annotated
from functools import lru_cache
from app.core.constants import DEFAULT_FRAMES_PATH, DEFAULT_VIDEOS_PATH
from app.schemas.config import AppConfig, DatabaseConfig, CeleryConfig


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter="__")

    app: AppConfig

    database: DatabaseConfig

    celery: CeleryConfig

    videos_path: str = DEFAULT_VIDEOS_PATH
    frames_path: str = DEFAULT_FRAMES_PATH


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

SettingsDep = Annotated[Settings, Depends(get_settings)]
