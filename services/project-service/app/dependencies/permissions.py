from collections.abc import Callable

from fastapi import (
    Depends,
    HTTPException,
    status,
)

from app.core.permissions import (
    Permission,
    has_permission,
)
from app.dependencies.security import (
    get_current_principal,
)
from app.schemas.principal import (
    AuthenticatedPrincipal,
)


def require_permission(
    permission: Permission,
) -> Callable:

    async def checker(
        principal:
            AuthenticatedPrincipal
            = Depends(
                get_current_principal
            ),
    ) -> AuthenticatedPrincipal:

        if not has_permission(
            principal.role,
            permission,
        ):
            raise HTTPException(
                status_code=(
                    status.HTTP_403_FORBIDDEN
                ),
                detail=(
                    "You do not have permission "
                    "to perform this action."
                ),
            )

        return principal

    return checker