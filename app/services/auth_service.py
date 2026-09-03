# app/services/auth_service.py
import hashlib
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
    generate_refresh_token
)
from app.db.models import User, UserRole
from app.exceptions.custom_exceptions import (
    AuthenticationFailedError,
    PermissionDeniedError,
    ResourceConflictError
)
from app.repositories.user_repository import UserRepository
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.schemas.auth import LoginRequest, LoginResponse, LogoutRequest, LogoutResponse, Tokens, RefreshTokenRequest
from app.schemas.user import UserResponse

class AuthService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)
        self.token_repo = RefreshTokenRepository(db)
        self.db = db

    async def _issue_tokens_for_user(self, user: User) -> Tokens:
        """Helper method to generate both tokens and save the refresh token session."""
        # 1. Generate Access Token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            subject=user.id,
            role=user.role,
            expires_delta=access_token_expires
        )

        # 2. Generate Refresh Token
        raw_refresh_token, token_hash = generate_refresh_token()
        
        # 3. Save to database
        expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        await self.token_repo.create(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=expires_at
        )

        return Tokens(
            access_token=access_token,
            refresh_token=raw_refresh_token,
            token_type="bearer"
        )

    async def authenticate_user(self, login_data: LoginRequest) -> LoginResponse:
        """Authenticates user credentials and issues both tokens."""
        user = await self.user_repo.get_by_email(login_data.email)
        
        if not user or not verify_password(login_data.password, user.password_hash):
            raise AuthenticationFailedError("Invalid email or password.")
        
        if not user.is_active:
            raise PermissionDeniedError("Account is deactivated. Please contact support.")
        
        tokens = await self._issue_tokens_for_user(user)
        
        return LoginResponse(
            user=UserResponse.model_validate(user),
            tokens=tokens
        )

    async def refresh_session(self, request: RefreshTokenRequest) -> Tokens:
        """Validates a refresh token and issues new tokens."""
        # 1. Hash the incoming raw token
        token_hash = hashlib.sha256(request.refresh_token.encode("utf-8")).hexdigest()
        
        # 2. Look it up in the database
        db_token = await self.token_repo.get_by_hash(token_hash)
        if not db_token:
            raise AuthenticationFailedError("Invalid refresh token.")
            
        # 3. Check if revoked
        if db_token.revoked_at is not None:
            # A revoked token is being used! We have a security breach.
            # Destroy all active sessions for this user.
            await self.token_repo.revoke_all_for_user(db_token.user_id)
            raise AuthenticationFailedError("Token reuse detected. All sessions terminated for security. Please log in again.")
            
        # 4. Check if expired
        token_expiration = db_token.expires_at
        if token_expiration.tzinfo is None:
            token_expiration = token_expiration.replace(tzinfo=timezone.utc)
            
        if token_expiration < datetime.now(timezone.utc):
            raise AuthenticationFailedError("Refresh token has expired.")
            
        # 5. Verify the user still exists and is active
        user = await self.user_repo.get_by_id(db_token.user_id)
        if not user or not user.is_active:
            raise PermissionDeniedError("User account is inactive or deleted.")

        # 6. Revoke the old token (Token Rotation)
        await self.token_repo.revoke(db_token)
        
        # 7. Issue completely new tokens
        return await self._issue_tokens_for_user(user)

    async def logout(self, request: LogoutRequest) -> LogoutResponse:
        """Finds the active refresh token and revokes it."""
        token_hash = hashlib.sha256(request.refresh_token.encode("utf-8")).hexdigest()
        db_token = await self.token_repo.get_by_hash(token_hash)
        
        if db_token and db_token.revoked_at is None:
            await self.token_repo.revoke(db_token)
            
        # We always return success even if the token was already dead, 
        # so attackers can't use this endpoint to guess valid tokens.
        return LogoutResponse(message="Successfully logged out.")