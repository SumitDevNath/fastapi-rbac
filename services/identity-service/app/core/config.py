from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

IDENTITY_SERVICE_DIR = Path(__file__).resolve().parents[2]
PROJECT_ROOT = IDENTITY_SERVICE_DIR.parents[1]

OLD_DB_PATH = PROJECT_ROOT / "app.db"

print("PROJECT_ROOT:", PROJECT_ROOT)
print("OLD_DB_PATH:", OLD_DB_PATH)

class Settings(BaseSettings):

    SERVICE_NAME: str = "identity-service"

    VERSION: str = "0.1.0"

    DATABASE_URL: str

    JWT_ALGORITHM: str = "RS256"

    JWT_PRIVATE_KEY_PATH: str

    JWT_PUBLIC_KEYS_DIR: str

    JWT_ACTIVE_KID: str

    JWT_ISSUER: str

    JWT_AUDIENCE: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15

    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()