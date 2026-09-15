from enum import Enum


class Permission(str, Enum):
    PROJECT_CREATE = "project:create"
    PROJECT_READ = "project:read"
    PROJECT_UPDATE = "project:update"
    PROJECT_DELETE = "project:delete"


ROLE_PERMISSIONS: dict[
    str,
    set[Permission],
] = {
    "ADMIN": {
        Permission.PROJECT_CREATE,
        Permission.PROJECT_READ,
        Permission.PROJECT_UPDATE,
        Permission.PROJECT_DELETE,
    },

    "MANAGER": {
        Permission.PROJECT_CREATE,
        Permission.PROJECT_READ,
        Permission.PROJECT_UPDATE,
        Permission.PROJECT_DELETE,
    },

    "EDITOR": {
        Permission.PROJECT_CREATE,
        Permission.PROJECT_READ,
        Permission.PROJECT_UPDATE,
    },

    # Preserve current wire value.
    "user": {
        Permission.PROJECT_READ,
    },
}


def has_permission(
    role: str,
    required_permission: Permission,
) -> bool:

    allowed = ROLE_PERMISSIONS.get(
        role,
        set(),
    )

    return required_permission in allowed