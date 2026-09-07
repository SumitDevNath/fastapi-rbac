from fastapi import (
    APIRouter,
    Depends,
    status,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.db.database import get_db
from app.dependencies.security import (
    get_current_principal,
)
from app.schemas.principal import (
    AuthenticatedPrincipal,
)
from app.schemas.profile import (
    ProfileCreate,
    ProfileResponse,
    ProfileUpdate,
)
from app.services.profile_service import (
    ProfileService,
)


router = APIRouter(
    prefix="/profiles",
    tags=["Profiles"],
)


@router.get(
    "/me",
    response_model=ProfileResponse,
)
async def get_my_profile(
    db: AsyncSession = Depends(get_db),
    principal: AuthenticatedPrincipal = Depends(
        get_current_principal
    ),
):
    return await ProfileService(
        db
    ).get_profile(
        principal.identity_id
    )


@router.post(
    "/me",
    response_model=ProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_my_profile(
    body: ProfileCreate,
    db: AsyncSession = Depends(get_db),
    principal: AuthenticatedPrincipal = Depends(
        get_current_principal
    ),
):
    return await ProfileService(
        db
    ).create_profile(
        principal.identity_id,
        body,
    )


@router.patch(
    "/me",
    response_model=ProfileResponse,
)
async def update_my_profile(
    body: ProfileUpdate,
    db: AsyncSession = Depends(get_db),
    principal: AuthenticatedPrincipal = Depends(
        get_current_principal
    ),
):
    return await ProfileService(
        db
    ).update_profile(
        principal.identity_id,
        body,
    )