from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.db.models import UserRole


class IdentityCreate(BaseModel):
    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128,
    )


class IdentityResponse(BaseModel):
    id: int
    email: EmailStr
    role: UserRole
    status: str | None
    auth_provider: str | None
    is_active: bool
    must_change_password: bool

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )