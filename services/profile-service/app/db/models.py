from datetime import (
    datetime,
    timezone,
)

from sqlalchemy import (
    DateTime,
    Integer,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.db.database import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    identity_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    username: Mapped[str | None] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=True,
    )

    hris_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    facility_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    lab_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    mobile: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    first_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    last_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    division_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    district_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    upazila_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    union_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(
            timezone.utc
        ),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(
            timezone.utc
        ),
        onupdate=lambda: datetime.now(
            timezone.utc
        ),
        nullable=False,
    )