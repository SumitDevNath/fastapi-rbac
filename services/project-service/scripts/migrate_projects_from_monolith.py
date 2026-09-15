import sqlite3
from pathlib import Path


SCRIPT_FILE = Path(__file__).resolve()

PROJECT_SERVICE_ROOT = (
    SCRIPT_FILE.parents[1]
)

MONOLITH_ROOT = (
    SCRIPT_FILE.parents[3]
)

SOURCE_DB = (
    MONOLITH_ROOT / "app.db"
)

TARGET_DB = (
    PROJECT_SERVICE_ROOT
    / "project.db"
)


def main():

    print(
        "Source:",
        SOURCE_DB,
    )

    print(
        "Target:",
        TARGET_DB,
    )

    source = sqlite3.connect(
        SOURCE_DB
    )

    target = sqlite3.connect(
        TARGET_DB
    )

    rows = source.execute(
        """
        SELECT
            id,
            title,
            description,
            owner_id,
            created_at,
            updated_at
        FROM projects
        ORDER BY id
        """
    ).fetchall()

    before = target.execute(
        """
        SELECT COUNT(*)
        FROM projects
        """
    ).fetchone()[0]

    for row in rows:
        target.execute(
            """
            INSERT INTO projects (
                id,
                title,
                description,
                owner_identity_id,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(id)
            DO NOTHING
            """,
            row,
        )

    target.commit()

    after = target.execute(
        """
        SELECT COUNT(*)
        FROM projects
        """
    ).fetchone()[0]

    print(
        "Source projects:",
        len(rows),
    )

    print(
        "Projects before:",
        before,
    )

    print(
        "Projects after:",
        after,
    )

    source.close()
    target.close()


if __name__ == "__main__":
    main()