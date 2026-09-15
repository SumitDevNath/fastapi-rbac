from fastapi import (
    APIRouter,
    Depends,
    Query,
    Response,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.permissions import Permission
from app.db.database import get_db
from app.dependencies.permissions import (
    require_permission,
)
from app.schemas.principal import (
    AuthenticatedPrincipal,
)
from app.schemas.project import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
)
from app.services.project_service import (
    ProjectService,
)


router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(
    project_in: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    principal: AuthenticatedPrincipal = Depends(
        require_permission(
            Permission.PROJECT_CREATE
        )
    ),
):
    service = ProjectService(db)

    return await service.create_project(
        project_in,
        owner_identity_id=(
            principal.identity_id
        ),
    )


@router.get(
    "",
    response_model=list[ProjectResponse],
)
async def list_projects(
    skip: int = Query(
        default=0,
        ge=0,
    ),
    limit: int = Query(
        default=50,
        ge=1,
        le=100,
    ),
    db: AsyncSession = Depends(get_db),
    principal: AuthenticatedPrincipal = Depends(
        require_permission(
            Permission.PROJECT_READ
        )
    ),
):
    service = ProjectService(db)

    return await service.list_projects(
        skip=skip,
        limit=limit,
    )


@router.get(
    "/my",
    response_model=list[ProjectResponse],
)
async def list_my_projects(
    skip: int = Query(
        default=0,
        ge=0,
    ),
    limit: int = Query(
        default=50,
        ge=1,
        le=100,
    ),
    db: AsyncSession = Depends(get_db),
    principal: AuthenticatedPrincipal = Depends(
        require_permission(
            Permission.PROJECT_READ
        )
    ),
):
    service = ProjectService(db)

    return await service.list_user_projects(
        identity_id=(
            principal.identity_id
        ),
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
)
async def get_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    principal: AuthenticatedPrincipal = Depends(
        require_permission(
            Permission.PROJECT_READ
        )
    ),
):
    return await ProjectService(
        db
    ).get_project(
        project_id
    )


@router.patch(
    "/{project_id}",
    response_model=ProjectResponse,
)
async def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    db: AsyncSession = Depends(get_db),
    principal: AuthenticatedPrincipal = Depends(
        require_permission(
            Permission.PROJECT_UPDATE
        )
    ),
):
    return await ProjectService(
        db
    ).update_project(
        project_id,
        project_update,
    )


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    principal: AuthenticatedPrincipal = Depends(
        require_permission(
            Permission.PROJECT_DELETE
        )
    ),
):
    await ProjectService(
        db
    ).delete_project(
        project_id
    )

    return Response(
        status_code=(
            status.HTTP_204_NO_CONTENT
        )
    )