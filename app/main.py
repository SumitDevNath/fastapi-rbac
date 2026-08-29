from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routes import health
from app.core.config import settings
from app.db.database import Base, engine
# Import models so Base.metadata detects them
import app.db.models  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables if they do not exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown: Dispose DB engine connection pool
    await engine.dispose()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(health.router, prefix=settings.API_V1_STR)


@app.get("/", tags=["Root"])
async def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "docs": "/docs",
        "health": f"{settings.API_V1_STR}/health"
    }