from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.auth import (
    LoginRequest,
    LogoutRequest,
    LogoutResponse,
    RefreshTokenRequest,
    Tokens,
)
from app.schemas.identity import (
    IdentityCreate,
    IdentityResponse,
)
from app.services.auth_service import AuthService
from app.services.identity_service import (
    IdentityService,
)


router = APIRouter(
    tags=["Identity"],
)


@router.post(
    "/identities",
    response_model=IdentityResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_identity(
    body: IdentityCreate,
    db: AsyncSession = Depends(get_db),
):
    return await IdentityService(
        db
    ).create_identity(body)

# Login route
@router.post(
    "/auth/login",
    status_code=status.HTTP_200_OK,
)
async def login(
    body: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    return await AuthService(db).authenticate(
        body
    )

# Refresh route
@router.post(
    "/auth/refresh",
    response_model=Tokens,
    status_code=status.HTTP_200_OK,
)
async def refresh(
    body: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
):
    return await AuthService(db).refresh(
        body
    )

# Logout route
@router.post(
    "/auth/logout",
    response_model=LogoutResponse,
)
async def logout(
    body: LogoutRequest,
    db: AsyncSession = Depends(get_db),
):
    return await AuthService(db).logout(
        body.refresh_token
    )
