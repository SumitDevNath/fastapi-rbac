# app/api/routes/auth.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.models import User
from app.dependencies.auth import get_current_user
from app.schemas.auth import (
    LoginRequest, 
    LoginResponse,
    LogoutRequest,
    LogoutResponse, 
    Tokens, 
    RefreshTokenRequest
)
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="User Login"
)
async def login(login_data: LoginRequest, db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    return await auth_service.authenticate_user(login_data)

@router.post(
    "/refresh",
    response_model=Tokens,
    status_code=status.HTTP_200_OK,
    summary="Refresh Access Token"
)
async def refresh_token(request: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    """
    Takes a raw refresh token, validates it against the database, 
    revokes it, and returns a fresh pair of access and refresh tokens.
    """
    auth_service = AuthService(db)
    return await auth_service.refresh_session(request)

@router.get(
    "/validate",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Validate Access Token"
)
async def validate_token(current_user: User = Depends(get_current_user)):
    """
    Accepts an Access Token in the Authorization header.
    If valid, returns the user's profile.
    """
    return current_user

@router.post(
    "/logout",
    response_model=LogoutResponse,
    status_code=status.HTTP_200_OK,
    summary="Logout User"
)
async def logout(request: LogoutRequest, db: AsyncSession = Depends(get_db)):
    """
    Revokes the provided refresh token so it can no longer be used.
    """
    auth_service = AuthService(db)
    return await auth_service.logout(request)