from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.user import UserResponse


# Shared properties across project schemas
class ProjectBase(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Project title.",
        examples=["API Security Audit"]
    )
    description: Optional[str] = Field(
        default=None,
        description="Optional detailed project description.",
        examples=["Complete internal review of auth endpoints and RBAC rules."]
    )


# Schema for Creating a Project (Input)
class ProjectCreate(ProjectBase):
    pass


# Schema for Updating a Project (Input)
class ProjectUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None


# Schema for Project Response (Output)
class ProjectResponse(ProjectBase):
    id: int
    owner_id: int
    owner: Optional[UserResponse] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)