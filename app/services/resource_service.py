from typing import List
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Project, User
from app.repositories.resource_repository import ProjectRepository
from app.schemas.resource import ProjectCreate, ProjectUpdate


class ProjectService:
    def __init__(self, db: AsyncSession):
        self.project_repo = ProjectRepository(db)

    async def create_project(self, project_in: ProjectCreate, current_user: User) -> Project:
        """Assigns the project to current_user and persists it."""
        return await self.project_repo.create(project_in, owner_id=current_user.id)

    async def get_project(self, project_id: int) -> Project:
        """Retrieves a project by ID or raises 404."""
        project = await self.project_repo.get_by_id(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with ID {project_id} not found."
            )
        return project

    async def list_projects(self, skip: int = 0, limit: int = 100) -> List[Project]:
        """Lists all projects with pagination parameters."""
        return await self.project_repo.list_all(skip=skip, limit=limit)

    async def update_project(
        self,
        project_id: int,
        project_update: ProjectUpdate
    ) -> Project:
        """Updates project details or raises 404."""
        project = await self.get_project(project_id)
        return await self.project_repo.update(project, project_update)

    async def delete_project(self, project_id: int) -> None:
        """Deletes a project record or raises 404."""
        project = await self.get_project(project_id)
        await self.project_repo.delete(project)