from fastapi import Depends, HTTPException, status
from app.core.permissions import Permission, has_permission
from app.db.models import User
from app.dependencies.auth import get_current_user


class PermissionChecker:
    """
    Callable dependency class that enforces granular permission checks.
    """
    def __init__(self, required_permission: Permission):
        self.required_permission = required_permission

    async def __call__(
        self,
        current_user: User = Depends(get_current_user)
    ) -> User:
        # Check if user's role contains the required permission
        if not has_permission(current_user.role, self.required_permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation not permitted. Required permission: '{self.required_permission.value}'"
            )
        return current_user


# Helper factory function for cleaner syntax in route signatures
def require_permission(permission: Permission) -> PermissionChecker:
    return PermissionChecker(permission)