from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
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
    """
    Registers a new user:
    - **email**: Must be a valid, unique RFC-compliant email address.
    - **password**: Must be between 8 and 128 characters.
    - **role**: Optional (defaults to VIEWER).
    """
    auth_service = AuthService(db)
    new_user = await auth_service.register_user(user_in)
    return new_user