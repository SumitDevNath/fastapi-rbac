from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.db.models import UserProfile


class ProfileRepository:
    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    async def get_by_identity_id(
        self,
        identity_id: int,
    ) -> UserProfile | None:

        stmt = select(
            UserProfile
        ).where(
            UserProfile.identity_id
            == identity_id
        )

        result = await self.db.execute(
            stmt
        )

        return result.scalar_one_or_none()

    async def get_by_username(
        self,
        username: str,
    ) -> UserProfile | None:

        stmt = select(
            UserProfile
        ).where(
            UserProfile.username
            == username
        )

        result = await self.db.execute(
            stmt
        )

        return result.scalar_one_or_none()

    async def create(
        self,
        profile: UserProfile,
    ) -> UserProfile:

        self.db.add(profile)

        await self.db.flush()

        return profile

    async def update(
        self,
        profile: UserProfile,
        update_data: dict,
    ) -> UserProfile:

        for field, value in (
            update_data.items()
        ):
            setattr(
                profile,
                field,
                value,
            )

        await self.db.flush()

        return profile