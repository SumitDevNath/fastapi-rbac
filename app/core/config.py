from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App Metadata
    PROJECT_NAME: str 
    VERSION: str
    API_V1_STR: str

    # Database
    DATABASE_URL: str

    # External Services
    DGHS_AUTH_VALIDATE_URL: str

    # CORS Whitelist (Parsed automatically from JSON or comma-separated string)
    CORS_ORIGINS: List[str]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()  # Will crash immediately if ANY key above is missing in .env