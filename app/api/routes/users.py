# app/api/routes/users.py
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.models import User, UserRole
from app.dependencies.auth import get_current_user
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.exceptions.custom_exceptions import PermissionDeniedError, ResourceConflictError, ResourceNotFoundError
from typing import List, Optional
from sqlalchemy import select
from app.dependencies.permissions import require_permission
from app.core.permissions import Permission
from app.schemas.user import UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create User"
)
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    """Creates a new user (Replaces old /auth/register)."""
    # SECURITY FIX: Force the role to standard 'user' regardless of what the payload says.
    # This prevents Mass Assignment attacks where hackers try to register as ADMIN.
    user_in.role = UserRole.USER
    user_repo = UserRepository(db)
    existing_user = await user_repo.get_by_email(user_in.email)
    if existing_user:
        raise ResourceConflictError("A user with this email address already exists.")
    
    return await user_repo.create(user_in)

@router.get(
    "",
    response_model=List[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="List all users"
)
async def list_users(
    role: Optional[str] = Query(default=None),
    status: Optional[str] = Query(default=None),
    facility_id: Optional[str] = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission(Permission.USER_READ))
):
    """
    Retrieves all users. Restricted to ADMIN and MANAGER via USER_READ permission.
    """
    stmt = select(User)
    
    if role:
        stmt = stmt.where(User.role == role)
    if status:
        stmt = stmt.where(User.status == status)
    if facility_id:
        stmt = stmt.where(User.facility_id == facility_id)
        
    stmt = stmt.offset(skip).limit(limit).order_by(User.id.asc())
    
    result = await db.execute(stmt)
    return list(result.scalars().all())

@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Me"
)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Returns the currently authenticated user's profile."""
    return current_user

@router.put(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Update User"
)
async def update_user(
    user_id: int, 
    user_update: UserUpdate, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)  # 1. Require authentication!
):
    """Updates user fields securely with field-level role checks."""
    
    # 2. Prevent users from editing OTHER users (unless they are an ADMIN)
    if current_user.id != user_id and current_user.role != UserRole.ADMIN:
        raise PermissionDeniedError("You do not have permission to update other users' profiles.")
        
    # 3. Prevent standard users from escalating privileges or approving themselves
    restricted_fields = {"status", "role", "is_active", "auth_provider"}
    update_data = user_update.model_dump(exclude_unset=True)
    
    # Check if the user is trying to change any of the restricted fields
    attempting_restricted_update = any(field in update_data for field in restricted_fields)
    
    if attempting_restricted_update and current_user.role != UserRole.ADMIN:
        raise PermissionDeniedError("Security violation: Only Administrators can modify account status, roles, or active states.")
        
    # 4. Proceed with the update if all security checks pass
    user_repo = UserRepository(db)
    target_user = await user_repo.get_by_id(user_id)
    if not target_user:
        raise ResourceNotFoundError(resource_name="User", identifier=user_id)
    
    return await user_repo.update(target_user, user_update)