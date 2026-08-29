from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App Metadata
    PROJECT_NAME: str
    VERSION: str
    API_V1_STR: str

    # Database
    DATABASE_URL: str

    # JWT Cryptographic Secrets
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # CORS Whitelist (Parsed automatically from JSON or comma-separated string)
    CORS_ORIGINS: List[str]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()  # Will crash immediately if ANY key above is missing in .env