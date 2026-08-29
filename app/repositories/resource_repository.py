from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.db.models import Project
from app.schemas.resource import ProjectCreate, ProjectUpdate


class ProjectRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, project_id: int) -> Optional[Project]:
        """
        Fetches a project by ID with the 'owner' relationship eagerly loaded.
        Generates optimized SQL using selectinload.
        """
        stmt = (
            select(Project)
            .where(Project.id == project_id)
            .options(selectinload(Project.owner))
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self, skip: int = 0, limit: int = 100) -> List[Project]:
        """
        Fetches paginated projects along with their owners.
        Executes exactly 2 SQL queries regardless of how many projects are returned (solves N+1).
        """
        stmt = (
            select(Project)
            .options(selectinload(Project.owner))
            .offset(skip)
            .limit(limit)
            .order_by(Project.id.desc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def list_by_owner(self, owner_id: int, skip: int = 0, limit: int = 100) -> List[Project]:
        """
        Fetches only projects belonging to a specific user (User-Scoped Isolation).
        """
        stmt = (
            select(Project)
            .where(Project.owner_id == owner_id)
            .options(selectinload(Project.owner))
            .offset(skip)
            .limit(limit)
            .order_by(Project.id.desc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, project_in: ProjectCreate, owner_id: int) -> Project:
        """Creates a project attached to owner_id."""
        db_project = Project(
            title=project_in.title,
            description=project_in.description,
            owner_id=owner_id
        )
        self.db.add(db_project)
        await self.db.commit()
        await self.db.refresh(db_project)
        return await self.get_by_id(db_project.id)  # type: ignore

    async def update(self, db_project: Project, project_update: ProjectUpdate) -> Project:
        """Partially updates project fields."""
        update_data = project_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_project, field, value)

        await self.db.commit()
        await self.db.refresh(db_project)
        return db_project

    async def delete(self, db_project: Project) -> None:
        """Deletes project from database."""
        await self.db.delete(db_project)
        await self.db.commit()