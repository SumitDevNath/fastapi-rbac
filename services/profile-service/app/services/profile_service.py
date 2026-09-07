from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.db.models import UserProfile
from app.exceptions.custom_exceptions import (
    ProfileAlreadyExistsError,
    ProfileNotFoundError,
    UsernameAlreadyExistsError,
)
from app.repositories.profile_repository import (
    ProfileRepository,
)
from app.schemas.profile import (
    ProfileCreate,
    ProfileUpdate,
)


class ProfileService:
    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db
        self.repo = ProfileRepository(db)

    async def get_profile(
        self,
        identity_id: int,
    ) -> UserProfile:

        profile = (
            await self.repo
            .get_by_identity_id(
                identity_id
            )
        )

        if profile is None:
            raise ProfileNotFoundError()

        return profile

    async def create_profile(
        self,
        identity_id: int,
        data: ProfileCreate,
    ) -> UserProfile:

        existing = (
            await self.repo
            .get_by_identity_id(
                identity_id
            )
        )

        if existing:
            raise ProfileAlreadyExistsError()

        if data.username:
            username_owner = (
                await self.repo
                .get_by_username(
                    data.username
                )
            )

            if username_owner:
                raise (
                    UsernameAlreadyExistsError()
                )

        profile = UserProfile(
            identity_id=identity_id,
            **data.model_dump(),
        )

        try:
            await self.repo.create(profile)
            await self.db.commit()
            await self.db.refresh(profile)

            return profile

        except IntegrityError as exc:
            await self.db.rollback()

            raise (
                UsernameAlreadyExistsError()
            ) from exc

    async def update_profile(
        self,
        identity_id: int,
        data: ProfileUpdate,
    ) -> UserProfile:

        profile = (
            await self.repo
            .get_by_identity_id(
                identity_id
            )
        )

        if profile is None:
            raise ProfileNotFoundError()

        update_data = data.model_dump(
            exclude_unset=True
        )

        new_username = update_data.get(
            "username"
        )

        if new_username:
            username_owner = (
                await self.repo
                .get_by_username(
                    new_username
                )
            )

            if (
                username_owner
                and
                username_owner.identity_id
                != identity_id
            ):
                raise (
                    UsernameAlreadyExistsError()
                )

        try:
            await self.repo.update(
                profile,
                update_data,
            )

            await self.db.commit()
            await self.db.refresh(profile)

            return profile

        except IntegrityError as exc:
            await self.db.rollback()

            raise (
                UsernameAlreadyExistsError()
            ) from exc