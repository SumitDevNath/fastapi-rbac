from datetime import datetime, timezone

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import RefreshSession


class RefreshSessionRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        *,
        identity_id: int,
        token_hash: str,
        expires_at: datetime,
    ) -> RefreshSession:

        session = RefreshSession(
            identity_id=identity_id,
            token_hash=token_hash,
            expires_at=expires_at,
        )

        self.db.add(session)

        await self.db.flush()

        return session

    async def get_by_hash(
        self,
        token_hash: str,
    ) -> RefreshSession | None:

        stmt = select(RefreshSession).where(
            RefreshSession.token_hash == token_hash
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def revoke(
        self,
        refresh_session: RefreshSession,
    ) -> None:

        refresh_session.revoked_at = (
            datetime.now(timezone.utc)
        )

        await self.db.flush()

    async def revoke_all_for_identity(
        self,
        identity_id: int,
    ) -> None:

        stmt = (
            update(RefreshSession)
            .where(
                RefreshSession.identity_id == identity_id
            )
            .where(
                RefreshSession.revoked_at.is_(None)
            )
            .values(
                revoked_at=datetime.now(timezone.utc)
            )
        )

        await self.db.execute(stmt)