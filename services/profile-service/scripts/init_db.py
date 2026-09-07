import asyncio

from app.db.database import (
    Base,
    engine,
)

# Important: register models
from app.db.models import UserProfile  # noqa: F401


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.create_all
        )

    print(
        "Profile database initialized."
    )


if __name__ == "__main__":
    asyncio.run(main())