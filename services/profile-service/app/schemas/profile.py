from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class ProfileEditableFields(BaseModel):
    username: str | None = Field(
        default=None,
        max_length=255,
    )

    facility_id: str | None = Field(
        default=None,
        max_length=255,
    )

    lab_id: str | None = Field(
        default=None,
        max_length=255,
    )

    mobile: str | None = Field(
        default=None,
        max_length=50,
    )

    first_name: str | None = Field(
        default=None,
        max_length=255,
    )

    last_name: str | None = Field(
        default=None,
        max_length=255,
    )

    division_id: str | None = Field(
        default=None,
        max_length=255,
    )

    district_id: str | None = Field(
        default=None,
        max_length=255,
    )

    upazila_id: str | None = Field(
        default=None,
        max_length=255,
    )

    union_id: str | None = Field(
        default=None,
        max_length=255,
    )

    model_config = ConfigDict(
        extra="forbid"
    )


class ProfileCreate(ProfileEditableFields):
    pass


class ProfileUpdate(ProfileEditableFields):
    pass


class ProfileResponse(ProfileEditableFields):
    identity_id: int

    # Stored by Profile Service,
    # but not self-editable yet.
    hris_id: str | None = None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )