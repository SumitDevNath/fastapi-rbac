from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes.auth import router
from app.core.config import settings
from app.db.database import engine
from app.exceptions.handlers import (
    register_exception_handlers,
)
from app.api.routes.jwks import (
    router as jwks_router,
)
from app.api.routes.auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()


app = FastAPI(
    title="Identity Service",
    version=settings.VERSION,
    lifespan=lifespan,
)


register_exception_handlers(app)


app.include_router(
    auth_router,
    prefix="/api/v1",
)

app.include_router(
    jwks_router,
)


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "identity-service",
    }