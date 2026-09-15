from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.custom_exceptions import (
    ProjectNotFoundError,
)


async def project_not_found_handler(
    request: Request,
    exc: ProjectNotFoundError,
):
    return JSONResponse(
        status_code=404,
        content={
            "error": {
                "code": "RESOURCE_NOT_FOUND",
                "message": (
                    f"Project with identifier "
                    f"'{exc.project_id}' "
                    "was not found."
                ),
                "details": None,
            }
        },
    )