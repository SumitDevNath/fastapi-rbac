from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.core.security import (
    create_access_token,
    get_password_hash,
    verify_password
)
from app.db.models import User, UserRole
from app.exceptions.custom_exceptions import (
    AuthenticationFailedError,
    PermissionDeniedError,
    ResourceConflictError
)
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserRegister, UserResponse


class AuthService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)

    async def register_user(self, user_in: UserRegister) -> User:
        """Registers a new user after verifying email uniqueness."""
        existing_user = await self.user_repo.get_by_email(user_in.email)
        if existing_user:
            raise ResourceConflictError("A user with this email address already exists.")

        hashed_password = get_password_hash(user_in.password)
        assigned_role = user_in.role or UserRole.VIEWER

        new_user = await self.user_repo.create(
            email=user_in.email,
            password_hash=hashed_password,
            role=assigned_role
        )
        return new_user

    async def authenticate_user(self, login_data: LoginRequest) -> TokenResponse:
        """Authenticates user credentials and issues a signed JWT."""
        user = await self.user_repo.get_by_email(login_data.email)
        # 2. Verify existence and password in constant time
        if not user or not verify_password(login_data.password, user.password_hash):
            raise AuthenticationFailedError("Invalid email or password.")

        if not user.is_active:
            raise PermissionDeniedError("Account is deactivated. Please contact support.")

        # 4. Generate signed JWT access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            subject=user.id,
            role=user.role.value,
            expires_delta=access_token_expires
        )

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserResponse.model_validate(user)
        )