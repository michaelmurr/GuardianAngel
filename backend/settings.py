import pathlib
from enum import Enum
from typing import Optional

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

from telemetry.schemas.decoder_schemas import DecodingSource

backend_directory = pathlib.Path(_file_).parent.parent
env_file_path = backend_directory.joinpath(".env")


class EnvMode(str, Enum):
    DEV = "DEV"
    PROD = "PROD"


class Settings(BaseSettings):
    app_name: str = "Live Viewer"
    app_version: str = "0.0.0"
    app_location: str = "dev"
    env_mode: EnvMode = EnvMode.DEV
    filestore_path: str = str(backend_directory.parent.joinpath("filestore"))

    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_host: str = "db"
    postgres_database: str = "postgres"
    postgres_port: int = 7001

    redis_host: str = "redis"
    redis_port: int = 6001


    model_config = SettingsConfigDict(env_file=env_file_path)


env = Settings()