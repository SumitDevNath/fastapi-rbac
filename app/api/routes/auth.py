from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserRegister, UserResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user account"
)
async def register(
    user_in: UserRegister,
    db: AsyncSession = Depends(get_db)
):
    """Registers a new user with email, password, and optional role."""
    auth_service = AuthService(db)
    new_user = await auth_service.register_user(user_in)
    return new_user


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="User Login / Issue Access Token"
)
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Authenticates credentials and returns a signed JWT access token.
    """
    auth_service = AuthService(db)
    return await auth_service.authenticate_user(login_data)