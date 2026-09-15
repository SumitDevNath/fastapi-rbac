from pathlib import Path

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


SERVICE_ROOT = Path(__file__).resolve().parents[2]

DEFAULT_PROJECT_DB = (
    SERVICE_ROOT / "project.db"
)


class Settings(BaseSettings):
    SERVICE_NAME: str = "project-service"
    VERSION: str = "0.1.0"

    DATABASE_URL: str = (
        "sqlite+aiosqlite:///"
        + DEFAULT_PROJECT_DB.as_posix()
    )

    IDENTITY_JWKS_URL: str = (
        "http://127.0.0.1:8001/"
        ".well-known/jwks.json"
    )

    JWT_ISSUER: str = (
        "http://127.0.0.1:8001"
    )

    JWT_AUDIENCE: str = "resource-api"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()