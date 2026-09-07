# app/repositories/identity_repository.py

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import IdentityAccount


class IdentityRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(
        self,
        identity_id: int,
    ) -> IdentityAccount | None:

        stmt = select(IdentityAccount).where(
            IdentityAccount.id == identity_id
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def get_by_email(
        self,
        email: str,
    ) -> IdentityAccount | None:

        stmt = select(IdentityAccount).where(
            IdentityAccount.email == email
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def create(
        self,
        *,
        email: str,
        password_hash: str,
    ) -> IdentityAccount:

        identity = IdentityAccount(
            email=email,
            password_hash=password_hash,
        )

        self.db.add(identity)

        await self.db.flush()
        await self.db.refresh(identity)

        return identity