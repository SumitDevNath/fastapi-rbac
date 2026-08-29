from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.permissions import Permission
from app.db.database import get_db
from app.db.models import User
from app.dependencies.permissions import require_permission
from app.schemas.resource import ProjectCreate, ProjectResponse, ProjectUpdate
from app.services.resource_service import ProjectService

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new project"
)
async def create_project(
    project_in: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission(Permission.PROJECT_CREATE))
):
    """
    Requires 'project:create' permission (Admin, Manager, Editor).
    """
    service = ProjectService(db)
    return await service.create_project(project_in, current_user)


@router.get(
    "",
    response_model=List[ProjectResponse],
    status_code=status.HTTP_200_OK,
    summary="List all projects"
)
async def list_projects(
    skip: int = Query(default=0, ge=0, description="Records to skip"),
    limit: int = Query(default=50, ge=1, le=100, description="Max records to return"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission(Permission.PROJECT_READ))
):
    """
    Requires 'project:read' permission (All roles).
    """
    service = ProjectService(db)
    return await service.list_projects(skip=skip, limit=limit)


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    status_code=status.HTTP_200_OK,
    summary="Get project by ID"
)
async def get_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission(Permission.PROJECT_READ))
):
    """
    Requires 'project:read' permission (All roles).
    """
    service = ProjectService(db)
    return await service.get_project(project_id)


@router.patch(
    "/{project_id}",
    response_model=ProjectResponse,
    status_code=status.HTTP_200_OK,
    summary="Update project"
)
async def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission(Permission.PROJECT_UPDATE))
):
    """
    Requires 'project:update' permission (Admin, Manager, Editor).
    """
    service = ProjectService(db)
    return await service.update_project(project_id, project_update)


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete project"
)
async def delete_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission(Permission.PROJECT_DELETE))
):
    """
    Requires 'project:delete' permission (Admin, Manager only).
    """
    service = ProjectService(db)
    await service.delete_project(project_id)