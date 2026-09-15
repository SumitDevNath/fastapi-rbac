from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class ProjectBase(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
    )

    description: str | None = None

    model_config = ConfigDict(
        extra="forbid"
    )


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

    description: str | None = None

    model_config = ConfigDict(
        extra="forbid"
    )


class ProjectResponse(ProjectBase):
    id: int

    owner_identity_id: int

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )