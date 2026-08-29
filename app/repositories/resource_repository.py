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
        """Fetch a single project by ID with owner data eagerly loaded."""
        stmt = (
            select(Project)
            .where(Project.id == project_id)
            .options(selectinload(Project.owner))
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self, skip: int = 0, limit: int = 100) -> List[Project]:
        """Fetch a paginated list of projects with owner data."""
        stmt = (
            select(Project)
            .options(selectinload(Project.owner))
            .offset(skip)
            .limit(limit)
            .order_by(Project.id.desc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, project_in: ProjectCreate, owner_id: int) -> Project:
        """Create and persist a new project record."""
        db_project = Project(
            title=project_in.title,
            description=project_in.description,
            owner_id=owner_id
        )
        self.db.add(db_project)
        await self.db.commit()
        await self.db.refresh(db_project)
        # Reload with owner relationship populated for response schema
        return await self.get_by_id(db_project.id)  # type: ignore

    async def update(self, db_project: Project, project_update: ProjectUpdate) -> Project:
        """Update existing project fields."""
        update_data = project_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_project, field, value)

        await self.db.commit()
        await self.db.refresh(db_project)
        return db_project

    async def delete(self, db_project: Project) -> None:
        """Delete a project record from SQLite."""
        await self.db.delete(db_project)
        await self.db.commit()