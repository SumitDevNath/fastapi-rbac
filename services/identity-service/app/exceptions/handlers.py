# app/exceptions/handlers.py

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse

from app.exceptions.custom_exceptions import (
    AuthenticationFailedError,
    PermissionDeniedError,
    ResourceConflictError,
)


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(ResourceConflictError)
    async def handle_resource_conflict(
        request: Request,
        exc: ResourceConflictError,
    ):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "error": {
                    "code": "RESOURCE_CONFLICT",
                    "message": exc.message,
                    "details": exc.details,
                }
            },
        )

    @app.exception_handler(AuthenticationFailedError)
    async def handle_authentication_failed(
        request: Request,
        exc: AuthenticationFailedError,
    ):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
            content={
                "error": {
                    "code": "AUTHENTICATION_FAILED",
                    "message": exc.message,
                    "details": exc.details,
                }
            },
        )

    @app.exception_handler(PermissionDeniedError)
    async def handle_permission_denied(
        request: Request,
        exc: PermissionDeniedError,
    ):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "error": {
                    "code": "FORBIDDEN",
                    "message": exc.message,
                    "details": exc.details,
                }
            },
        )

    @app.exception_handler(HTTPException)
    async def handle_http_exception(
        request: Request,
        exc: HTTPException,
    ):
        return JSONResponse(
            status_code=exc.status_code,
            headers=exc.headers,
            content={
                "error": {
                    "code": "HTTP_ERROR",
                    "message": exc.detail,
                    "details": None,
                }
            },
        )

    @app.exception_handler(Exception)
    async def handle_unhandled_exception(
        request: Request,
        exc: Exception,
    ):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": (
                        "An unexpected server error occurred."
                    ),
                    "details": None,
                }
            },
        )