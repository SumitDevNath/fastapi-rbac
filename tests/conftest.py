import os
from typing import AsyncGenerator
import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# Set test environment variables BEFORE importing app config
os.environ["JWT_SECRET_KEY"] = "test-secret-key-32-chars-minimum-entropy!!"
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

from app.core.security import create_access_token
from app.db.database import Base, get_db
from app.db.models import UserRole
from app.main import app

# 1. Create In-Memory SQLite Engine
test_engine = create_async_engine(
    "sqlite+aiosqlite:///:memory:",
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


# 2. Database Session Fixture (Isolated tables per test)
@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# 3. Async HTTP Client Fixture
@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


# 4. Helper Fixture for Tokens
@pytest.fixture
def create_token():
    def _create_token(user_id: int, role: UserRole) -> str:
        return create_access_token(subject=user_id, role=role.value)
    return _create_token