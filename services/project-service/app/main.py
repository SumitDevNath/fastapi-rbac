from fastapi import FastAPI

from app.api.routes.health import (
    router as health_router,
)
from app.api.routes.projects import (
    router as project_router,
)
from app.core.config import settings
from app.exceptions.custom_exceptions import (
    ProjectNotFoundError,
)
from app.exceptions.handlers import (
    project_not_found_handler,
)


app = FastAPI(
    title="Project Service",
    version=settings.VERSION,
)


app.add_exception_handler(
    ProjectNotFoundError,
    project_not_found_handler,
)


app.include_router(
    health_router
)

app.include_router(
    project_router,
    prefix="/api/v1",
)