from pydantic import BaseModel

from app.enums.app_env import AppEnv


class AppConfig(BaseModel):
    debug: bool = False
    env: AppEnv = AppEnv.DEVELOPMENT
