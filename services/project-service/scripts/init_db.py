import asyncio

from app.db.database import (
    Base,
    engine,
)

from app.db.models import Project  # noqa: F401


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.create_all
        )

    print(
        "Project database initialized."
    )


if __name__ == "__main__":
    asyncio.run(main())