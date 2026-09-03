from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.exceptions.custom_exceptions import (
    AuthenticationFailedError,
    PermissionDeniedError,
    ResourceConflictError,
    ResourceNotFoundError,
)


def register_exception_handlers(app: FastAPI) -> None:
    """
    Registers global exception handlers across the FastAPI application.
    """

    @app.exception_handler(ResourceNotFoundError)
    async def handle_resource_not_found(request: Request, exc: ResourceNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": {
                    "code": "RESOURCE_NOT_FOUND",
                    "message": exc.message,
                    "details": exc.details
                }
            }
        )

    @app.exception_handler(ResourceConflictError)
    async def handle_resource_conflict(request: Request, exc: ResourceConflictError):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "error": {
                    "code": "RESOURCE_CONFLICT",
                    "message": exc.message,
                    "details": exc.details
                }
            }
        )

    @app.exception_handler(AuthenticationFailedError)
    async def handle_auth_failed(request: Request, exc: AuthenticationFailedError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
            content={
                "error": {
                    "code": "AUTHENTICATION_FAILED",
                    "message": exc.message,
                    "details": exc.details
                }
            }
        )

    @app.exception_handler(PermissionDeniedError)
    async def handle_permission_denied(request: Request, exc: PermissionDeniedError):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "error": {
                    "code": "FORBIDDEN",
                    "message": exc.message,
                    "details": exc.details
                }
            }
        )

    @app.exception_handler(HTTPException)
    async def handle_http_exception(request: Request, exc: HTTPException):
        code_map = {
            400: "BAD_REQUEST",
            401: "AUTHENTICATION_FAILED",
            403: "FORBIDDEN",
            404: "NOT_FOUND",
            409: "RESOURCE_CONFLICT",
        }
        code = code_map.get(exc.status_code, "HTTP_ERROR")
        return JSONResponse(
            status_code=exc.status_code,
            headers=exc.headers,
            content={
                "error": {
                    "code": code,
                    "message": exc.detail,
                    "details": None
                }
            }
        )

    # @app.exception_handler(RequestValidationError)
    # async def handle_validation_error(request: Request, exc: RequestValidationError):
    #     # Format Pydantic errors into a clean, unified structure
    #     errors = []
    #     for err in exc.errors():
    #         field = " -> ".join(str(loc) for loc in err.get("loc", []))
    #         errors.append({
    #             "field": field,
    #             "issue": err.get("msg"),
    #             "type": err.get("type")
    #         })

    #     return JSONResponse(
    #         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    #         content={
    #             "error": {
    #                 "code": "VALIDATION_ERROR",
    #                 "message": "The request body or query parameters failed schema validation.",
    #                 "details": errors
    #             }
    #         }
    #     )

    @app.exception_handler(Exception)
    async def handle_unhandled_exception(request: Request, exc: Exception):
        # In production: Log the full traceback to Sentry / Datadog
        # Never leak raw stack traces to the public internet in the response body!
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected server error occurred. Please try again later.",
                    "details": None
                }
            }
        )