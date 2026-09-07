# app/services/identity_service.py

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.exceptions.custom_exceptions import (
    ResourceConflictError,
)
from app.repositories.identity_repository import (
    IdentityRepository,
)
from app.schemas.identity import (
    IdentityCreate,
    IdentityResponse,
)


class IdentityService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = IdentityRepository(db)

    async def create_identity(
        self,
        data: IdentityCreate,
    ) -> IdentityResponse:

        existing = await self.repo.get_by_email(
            data.email
        )

        if existing:
            raise ResourceConflictError(
                "A user with this email address "
                "already exists."
            )

        password_hash = hash_password(
            data.password
        )

        try:
            identity = await self.repo.create(
                email=data.email,
                password_hash=password_hash,
            )

            await self.db.commit()

        except IntegrityError:
            await self.db.rollback()

            raise ResourceConflictError(
                "A user with this email address "
                "already exists."
            )

        return IdentityResponse.model_validate(
            identity
        )