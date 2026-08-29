import enum
from typing import Set
from app.db.models import UserRole


class Permission(str, enum.Enum):
    # User Management Permissions
    USER_READ = "user:read"
    USER_MANAGE = "user:manage"

    # Project Resource Permissions
    PROJECT_CREATE = "project:create"
    PROJECT_READ = "project:read"
    PROJECT_UPDATE = "project:update"
    PROJECT_DELETE = "project:delete"


# Central Role-to-Permission Mapping Matrix
ROLE_PERMISSIONS: dict[UserRole, Set[Permission]] = {
    UserRole.ADMIN: {
        Permission.USER_READ,
        Permission.USER_MANAGE,
        Permission.PROJECT_CREATE,
        Permission.PROJECT_READ,
        Permission.PROJECT_UPDATE,
        Permission.PROJECT_DELETE,
    },
    UserRole.MANAGER: {
        Permission.USER_READ,
        Permission.PROJECT_CREATE,
        Permission.PROJECT_READ,
        Permission.PROJECT_UPDATE,
        Permission.PROJECT_DELETE,
    },
    UserRole.EDITOR: {
        Permission.PROJECT_CREATE,
        Permission.PROJECT_READ,
        Permission.PROJECT_UPDATE,
    },
    UserRole.VIEWER: {
        Permission.PROJECT_READ,
    },
}


def has_permission(user_role: UserRole, required_permission: Permission) -> bool:
    """
    Evaluates whether a given UserRole possesses the required permission.
    """
    allowed_permissions = ROLE_PERMISSIONS.get(user_role, set())
    return required_permission in allowed_permissions