from fastapi import Depends
from app.core.permissions import Permission, has_permission
from app.db.models import User
from app.dependencies.auth import get_current_user
from app.exceptions.custom_exceptions import PermissionDeniedError


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
        if not has_permission(current_user.role, self.required_permission):
            raise PermissionDeniedError(
                f"Operation not permitted. Required permission: '{self.required_permission.value}'"
            )
        return current_user


# Helper factory function for cleaner syntax in route signatures
def require_permission(permission: Permission) -> PermissionChecker:
    return PermissionChecker(permission)