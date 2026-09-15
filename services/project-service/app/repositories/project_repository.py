from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Project


class ProjectRepository:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    async def get_by_id(
        self,
        project_id: int,
    ) -> Project | None:

        stmt = select(Project).where(
            Project.id == project_id
        )

        result = await self.db.execute(
            stmt
        )

        return result.scalar_one_or_none()

    async def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Project]:

        stmt = (
            select(Project)
            .offset(skip)
            .limit(limit)
            .order_by(Project.id.desc())
        )

        result = await self.db.execute(
            stmt
        )

        return list(
            result.scalars().all()
        )

    async def list_by_owner(
        self,
        owner_identity_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Project]:

        stmt = (
            select(Project)
            .where(
                Project.owner_identity_id
                == owner_identity_id
            )
            .offset(skip)
            .limit(limit)
            .order_by(Project.id.desc())
        )

        result = await self.db.execute(
            stmt
        )

        return list(
            result.scalars().all()
        )

    async def create(
        self,
        project: Project,
    ) -> Project:

        self.db.add(project)

        await self.db.flush()

        return project

    async def update(
        self,
        project: Project,
        update_data: dict,
    ) -> Project:

        for field, value in (
            update_data.items()
        ):
            setattr(
                project,
                field,
                value,
            )

        await self.db.flush()

        return project

    async def delete(
        self,
        project: Project,
    ) -> None:

        await self.db.delete(project)

        await self.db.flush()