from fastapi import FastAPI

from app.api.routes.health import (
    router as health_router,
)
from app.api.routes.profiles import (
    router as profile_router,
)
from app.core.config import settings
from app.exceptions.custom_exceptions import (
    ProfileAlreadyExistsError,
    ProfileNotFoundError,
    UsernameAlreadyExistsError,
)
from app.exceptions.handlers import (
    profile_exists_handler,
    profile_not_found_handler,
    username_exists_handler,
)


app = FastAPI(
    title="Profile Service",
    version=settings.VERSION,
)


app.add_exception_handler(
    ProfileNotFoundError,
    profile_not_found_handler,
)

app.add_exception_handler(
    ProfileAlreadyExistsError,
    profile_exists_handler,
)

app.add_exception_handler(
    UsernameAlreadyExistsError,
    username_exists_handler,
)


app.include_router(
    health_router,
)

app.include_router(
    profile_router,
    prefix="/api/v1",
)