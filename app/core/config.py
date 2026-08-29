from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Enterprise Auth & RBAC Service"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # SQLite Database URL (Async driver: aiosqlite)
    DATABASE_URL: str = "sqlite+aiosqlite:///./app.db"

    # JWT Cryptographic Settings (Loaded from environment in production)
    JWT_SECRET_KEY: str = "insecure-development-secret-key-change-in-production-min-32-chars"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


settings = Settings()