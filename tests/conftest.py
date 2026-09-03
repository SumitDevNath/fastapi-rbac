import pytest
from datetime import timedelta
from app.core.security import create_access_token
import pytest_asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.main import app
from app.db.database import Base, get_db
from app.core.config import settings

# Dedicated in-memory / temporary test database
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestAsyncSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

@pytest_asyncio.fixture(scope="session", autouse=True, loop_scope="session")
async def init_test_db():
    """Initializes tables before tests run and disposes engine afterward."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()

@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Provides a transactional database session per test."""
    async with TestAsyncSessionLocal() as session:
        yield session
        await session.rollback()

@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Provides an httpx AsyncClient with database session dependency overridden."""
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
        
    app.dependency_overrides.clear()

@pytest.fixture
def create_token():
    def _create_token(user_id: int, role: str):
        # Handle if an Enum is passed instead of a string
        role_str = role.value if hasattr(role, "value") else role
        return create_access_token(
            subject=user_id,
            role=role_str,
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
    return _create_token