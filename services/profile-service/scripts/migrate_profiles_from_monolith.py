import sqlite3
from pathlib import Path


SCRIPT_FILE = Path(__file__).resolve()

PROFILE_SERVICE_ROOT = (
    SCRIPT_FILE.parents[1]
)

PROJECT_ROOT = (
    SCRIPT_FILE.parents[3]
)


SOURCE_DB = PROJECT_ROOT / "app.db"

TARGET_DB = (
    PROFILE_SERVICE_ROOT
    / "profile.db"
)


PROFILE_COLUMNS = [
    "id",
    "username",
    "hris_id",
    "facility_id",
    "lab_id",
    "mobile",
    "first_name",
    "last_name",
    "division_id",
    "district_id",
    "upazila_id",
    "union_id",
    "created_at",
    "updated_at",
]


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
            username,
            hris_id,
            facility_id,
            lab_id,
            mobile,
            first_name,
            last_name,
            division_id,
            district_id,
            upazila_id,
            union_id,
            created_at,
            updated_at
        FROM users
        """
    ).fetchall()

    before = target.execute(
        """
        SELECT COUNT(*)
        FROM user_profiles
        """
    ).fetchone()[0]

    for row in rows:
        target.execute(
            """
            INSERT INTO user_profiles (
                identity_id,
                username,
                hris_id,
                facility_id,
                lab_id,
                mobile,
                first_name,
                last_name,
                division_id,
                district_id,
                upazila_id,
                union_id,
                created_at,
                updated_at
            )
            VALUES (
                ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?
            )
            ON CONFLICT(identity_id)
            DO NOTHING
            """,
            row,
        )

    target.commit()

    after = target.execute(
        """
        SELECT COUNT(*)
        FROM user_profiles
        """
    ).fetchone()[0]

    print(
        "Source users:",
        len(rows),
    )

    print(
        "Profiles before:",
        before,
    )

    print(
        "Profiles after:",
        after,
    )

    source.close()
    target.close()


if __name__ == "__main__":
    main()