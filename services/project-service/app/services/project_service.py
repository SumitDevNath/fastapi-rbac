from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Project
from app.exceptions.custom_exceptions import (
    ProjectNotFoundError,
)
from app.repositories.project_repository import (
    ProjectRepository,
)
from app.schemas.project import (
    ProjectCreate,
    ProjectUpdate,
)


class ProjectService:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db
        self.repo = ProjectRepository(db)

    async def create_project(
        self,
        data: ProjectCreate,
        owner_identity_id: int,
    ) -> Project:

        project = Project(
            title=data.title,
            description=data.description,
            owner_identity_id=owner_identity_id,
        )

        await self.repo.create(
            project
        )

        await self.db.commit()
        await self.db.refresh(project)

        return project

    async def get_project(
        self,
        project_id: int,
    ) -> Project:

        project = await self.repo.get_by_id(
            project_id
        )

        if project is None:
            raise ProjectNotFoundError(
                project_id
            )

        return project

    async def list_projects(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Project]:

        return await self.repo.list_all(
            skip=skip,
            limit=limit,
        )

    async def list_user_projects(
        self,
        identity_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Project]:

        return await self.repo.list_by_owner(
            owner_identity_id=identity_id,
            skip=skip,
            limit=limit,
        )

    async def update_project(
        self,
        project_id: int,
        data: ProjectUpdate,
    ) -> Project:

        project = await self.get_project(
            project_id
        )

        update_data = data.model_dump(
            exclude_unset=True
        )

        await self.repo.update(
            project,
            update_data,
        )

        await self.db.commit()
        await self.db.refresh(project)

        return project

    async def delete_project(
        self,
        project_id: int,
    ) -> None:

        project = await self.get_project(
            project_id
        )

        await self.repo.delete(
            project
        )

        await self.db.commit()