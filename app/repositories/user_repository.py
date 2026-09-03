from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: int) -> Optional[User]:
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, user_in: UserCreate) -> User:
        """Instantiates and commits a new User record with dynamic fields."""
        hashed_password = get_password_hash(user_in.password)
        
        # Convert schema to dict, exclude password, and add the hashed password
        user_data = user_in.model_dump(exclude={"password"}, exclude_unset=True)
        user_data["password_hash"] = hashed_password
        
        db_user = User(**user_data)
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def update(self, db_user: User, user_update: UserUpdate) -> User:
        """Partially updates user fields."""
        update_data = user_update.model_dump(exclude_unset=True)
        
        if "password" in update_data:
            update_data["password_hash"] = get_password_hash(update_data.pop("password"))
            
        for field, value in update_data.items():
            setattr(db_user, field, value)
            
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user