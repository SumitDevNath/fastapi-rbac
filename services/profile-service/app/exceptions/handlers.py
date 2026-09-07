from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.custom_exceptions import (
    ProfileAlreadyExistsError,
    ProfileNotFoundError,
    UsernameAlreadyExistsError,
)


async def profile_not_found_handler(
    request: Request,
    exc: ProfileNotFoundError,
):
    return JSONResponse(
        status_code=404,
        content={
            "error": {
                "code": "PROFILE_NOT_FOUND",
                "message": (
                    "Profile was not found."
                ),
                "details": None,
            }
        },
    )


async def profile_exists_handler(
    request: Request,
    exc: ProfileAlreadyExistsError,
):
    return JSONResponse(
        status_code=409,
        content={
            "error": {
                "code": (
                    "PROFILE_ALREADY_EXISTS"
                ),
                "message": (
                    "Profile already exists."
                ),
                "details": None,
            }
        },
    )


async def username_exists_handler(
    request: Request,
    exc: UsernameAlreadyExistsError,
):
    return JSONResponse(
        status_code=409,
        content={
            "error": {
                "code": (
                    "USERNAME_ALREADY_EXISTS"
                ),
                "message": (
                    "Username is already in use."
                ),
                "details": None,
            }
        },
    )