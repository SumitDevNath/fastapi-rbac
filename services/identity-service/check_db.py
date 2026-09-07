import asyncio

from sqlalchemy import text

from app.db.database import engine


async def main():
    print("ENGINE URL:", engine.url)

    async with engine.connect() as connection:
        result = await connection.execute(
            text(
                """
                SELECT name
                FROM sqlite_master
                WHERE type='table'
                """
            )
        )

        print("TABLES:", result.fetchall())

        result = await connection.execute(
            text(
                """
                SELECT id, email
                FROM users
                LIMIT 5
                """
            )
        )

        print("USERS:", result.fetchall())

        result = await connection.execute(
            text("PRAGMA database_list")
        )

        print("DATABASE LIST:")
        for row in result.fetchall():
            print(row)


asyncio.run(main())