from fastapi import APIRouter

from app.core.jwks import load_jwks


router = APIRouter(
    tags=["Security"],
)


@router.get(
    "/.well-known/jwks.json",
)
async def get_jwks():
    return load_jwks()