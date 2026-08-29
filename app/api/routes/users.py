from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.permissions import Permission
from app.db.database import get_db
from app.db.models import User
from app.dependencies.auth import get_current_user
from app.dependencies.permissions import require_permission
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Current User Profile"
)
async def read_users_me(
    current_user: User = Depends(get_current_user)
):
    """Accessible by ANY authenticated user."""
    return current_user


@router.get(
    "",
    response_model=List[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="List all users (Admin & Manager only)"
)
async def list_users(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission(Permission.USER_READ))
):
    """
    Requires 'user:read' permission (Admin & Manager).
    """
    stmt = select(User).order_by(User.id)
    result = await db.execute(stmt)
    users = result.scalars().all()
    return users


@router.patch(
    "/{user_id}/role",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Update user role or status (Admin only)"
)
async def update_user_role(
    user_id: int,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission(Permission.USER_MANAGE))
):
    """
    Requires 'user:manage' permission (Admin only).
    """
    user_repo = UserRepository(db)
    target_user = await user_repo.get_by_id(user_id)

    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    if user_update.role is not None:
        target_user.role = user_update.role
    if user_update.is_active is not None:
        target_user.is_active = user_update.is_active

    await db.commit()
    await db.refresh(target_user)
    return target_user