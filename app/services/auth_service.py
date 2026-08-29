from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import get_password_hash
from app.db.models import User, UserRole
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserRegister


class AuthService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)

    async def register_user(self, user_in: UserRegister) -> User:
        """
        Orchestrates user registration:
        1. Checks if email is already taken.
        2. Hashes the plaintext password.
        3. Persists the user record.
        """
        # 1. Check for duplicate email
        existing_user = await self.user_repo.get_by_email(user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A user with this email address already exists."
            )

        # 2. Hash password securely using Argon2id
        hashed_password = get_password_hash(user_in.password)

        # 3. Create and persist user record (defaults to VIEWER if not provided)
        assigned_role = user_in.role or UserRole.VIEWER
        new_user = await self.user_repo.create(
            email=user_in.email,
            password_hash=hashed_password,
            role=assigned_role
        )

        return new_user