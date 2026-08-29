from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

# 1. Create Async Engine
# connect_args={"check_same_thread": False} is required only for SQLite
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,  # Set to True if you want to inspect raw SQL queries in console
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# 2. Create Async Session Factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Prevents attributes from expiring after commit
    autoflush=False
)


# 3. Base Class for all SQLAlchemy Models
class Base(DeclarativeBase):
    pass


# 4. Dependency to yield database session per HTTP request
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()