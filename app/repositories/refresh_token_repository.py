# app/repositories/refresh_token_repository.py
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import RefreshToken

class RefreshTokenRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_id: int, token_hash: str, expires_at: datetime) -> RefreshToken:
        """Stores a new refresh token hash in the database."""
        db_token = RefreshToken(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at
        )
        self.db.add(db_token)
        await self.db.commit()
        await self.db.refresh(db_token)
        return db_token

    async def get_by_hash(self, token_hash: str) -> Optional[RefreshToken]:
        """Finds a refresh token record by its SHA-256 hash."""
        stmt = select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def revoke(self, db_token: RefreshToken) -> None:
        """Soft-deletes a token by setting the revoked_at timestamp."""
        db_token.revoked_at = datetime.now(timezone.utc)
        await self.db.commit()

    async def revoke_all_for_user(self, user_id: int) -> None:
        """Instantly revokes every active token for a compromised user."""
        stmt = (
            update(RefreshToken)
            .where(RefreshToken.user_id == user_id)
            .where(RefreshToken.revoked_at.is_(None))
            .values(revoked_at=datetime.now(timezone.utc))
        )
        await self.db.execute(stmt)
        await self.db.commit()