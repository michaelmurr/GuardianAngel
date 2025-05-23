import pathlib
from enum import Enum

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

backend_directory = pathlib.Path(__file__).parent
env_file_path = backend_directory.joinpath(".env")

print(env_file_path)


class EnvMode(str, Enum):
    DEV = "DEV"
    PROD = "PROD"


class Settings(BaseSettings):
    REDIS_URL: str = "url"
    PTG_URL: str = "postgres"
    PTG_DB_NAME: str = "db"
    PG_HOST: str = "0.0.0"
    PTG_PORT: int = 7001

    PTG_USER: str = "user"
    PTG_PWD: str = "pwd"

    CLERK_PUBLISHABLE_KEY: str
    CLERK_SECRET_KEY: str
    CLERK_JWKS_URL: str

    GOOGLE_MAPS_API_KEY: str
    model_config = SettingsConfigDict(env_file=env_file_path)


env = Settings()
