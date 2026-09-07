# app/services/auth_service.py

from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import (
    create_access_token,
    generate_refresh_token,
    hash_refresh_token,
    verify_password,
)
from app.exceptions.custom_exceptions import (
    AuthenticationFailedError,
    PermissionDeniedError,
)
from app.repositories.identity_repository import (
    IdentityRepository,
)
from app.repositories.refresh_session_repository import (
    RefreshSessionRepository,
)
from app.schemas.auth import (
    LoginRequest,
    LogoutResponse,
    RefreshTokenRequest,
    Tokens,
)
from app.schemas.identity import IdentityResponse


class AuthService:

    def __init__(self, db: AsyncSession):
        self.db = db

        self.identity_repo = IdentityRepository(db)

        self.refresh_repo = (
            RefreshSessionRepository(db)
        )

    async def _create_token_pair(
        self,
        identity,
    ) -> Tokens:

        access_token = create_access_token(
            subject=identity.id,
            role=identity.role,
            expires_delta=timedelta(
                minutes=(
                    settings
                    .ACCESS_TOKEN_EXPIRE_MINUTES
                )
            ),
        )

        raw_refresh_token, token_hash = (
            generate_refresh_token()
        )

        expires_at = (
            datetime.now(timezone.utc)
            + timedelta(
                days=(
                    settings
                    .REFRESH_TOKEN_EXPIRE_DAYS
                )
            )
        )

        await self.refresh_repo.create(
            identity_id=identity.id,
            token_hash=token_hash,
            expires_at=expires_at,
        )

        return Tokens(
            access_token=access_token,
            refresh_token=raw_refresh_token,
        )

    # Login transaction
    async def authenticate(
        self,
        login_data: LoginRequest,
    ):

        identity = (
            await self.identity_repo.get_by_email(
                login_data.email
            )
        )

        if (
            identity is None
            or not verify_password(
                login_data.password,
                identity.password_hash,
            )
        ):
            raise AuthenticationFailedError(
                "Invalid email or password."
            )

        if not identity.is_active:
            raise PermissionDeniedError(
                "Account is deactivated. "
                "Please contact support."
            )

        tokens = await self._create_token_pair(
            identity
        )

        await self.db.commit()

        return {
            "identity": IdentityResponse.model_validate(
                identity
            ),
            "tokens": tokens,
        }

    # Refresh transaction
    async def refresh(
        self,
        request: RefreshTokenRequest,
    ) -> Tokens:

        token_hash = hash_refresh_token(
            request.refresh_token
        )

        old_session = (
            await self.refresh_repo.get_by_hash(
                token_hash
            )
        )

        if old_session is None:
            raise AuthenticationFailedError(
                "Invalid refresh token."
            )

        if old_session.revoked_at is not None:

            await (
                self.refresh_repo
                .revoke_all_for_identity(
                    old_session.identity_id
                )
            )

            await self.db.commit()

            raise AuthenticationFailedError(
                "Token reuse detected. "
                "All sessions terminated for security."
            )

        expiration = old_session.expires_at

        if expiration.tzinfo is None:
            expiration = expiration.replace(
                tzinfo=timezone.utc
            )

        if expiration < datetime.now(timezone.utc):
            raise AuthenticationFailedError(
                "Refresh token has expired."
            )

        identity = (
            await self.identity_repo.get_by_id(
                old_session.identity_id
            )
        )

        if identity is None or not identity.is_active:
            raise PermissionDeniedError(
                "User account is inactive or deleted."
            )

        await self.refresh_repo.revoke(
            old_session
        )

        new_tokens = await self._create_token_pair(
            identity
        )

        await self.db.commit()

        return new_tokens

    # Logout
    async def logout(
        self,
        raw_refresh_token: str,
    ) -> LogoutResponse:

        token_hash = hash_refresh_token(
            raw_refresh_token
        )

        session = (
            await self.refresh_repo.get_by_hash(
                token_hash
            )
        )

        if (
            session is not None
            and session.revoked_at is None
        ):
            await self.refresh_repo.revoke(session)

            await self.db.commit()

        return LogoutResponse(
            message="Successfully logged out."
        )