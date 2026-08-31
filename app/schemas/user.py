from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from app.db.models import UserRole


# Shared properties across user schemas. This class defines the common fields that are shared by multiple user-related schemas. so userregister, userupdate, userresponse will inherit from this class. This promotes code reusability and consistency across the application.
class UserBase(BaseModel):
    email: EmailStr = Field(
        ...,
        description="Valid email address adhering to RFC standards.",
        examples=["alice@example.com"]
    )


# Schema for User Registration (Input)
class UserRegister(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Plaintext password. Must be between 8 and 128 characters.",
        examples=["SecurePass123!"]
    )
    role: Optional[UserRole] = Field(
        default=UserRole.VIEWER,
        description="User role in the system. Defaults to VIEWER."
    )


# Schema for Updating User Details (Input - Admin only)
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


# Safe Schema for returning User data to clients (Output)
class UserResponse(UserBase):
    id: int
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime

    # Pydantic v2 configuration to read data from SQLAlchemy ORM objects
    model_config = ConfigDict(from_attributes=True)