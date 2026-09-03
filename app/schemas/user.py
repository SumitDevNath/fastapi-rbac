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
class UserCreate(UserBase):
    username: Optional[str] = None
    email: EmailStr
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Plaintext password. Must be between 8 and 128 characters.",
        examples=["SecurePass123!"]
    )
    role: UserRole = Field(
        default=UserRole.USER,
        description="User role in the system. Defaults to USER."
    )
    status: Optional[str] = "pending"
    auth_provider: Optional[str] = "local"
    facility_id: Optional[str] = None
    lab_id: Optional[str] = None
    mobile: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    division_id: Optional[str] = None
    district_id: Optional[str] = None
    upazila_id: Optional[str] = None
    union_id: Optional[str] = None


# Schema for Updating User Details (Input - Admin only)
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None
    status: Optional[str] = None
    auth_provider: Optional[str] = None
    facility_id: Optional[str] = None
    lab_id: Optional[str] = None
    mobile: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    division_id: Optional[str] = None
    district_id: Optional[str] = None
    upazila_id: Optional[str] = None
    union_id: Optional[str] = None
    is_active: Optional[bool] = None


# Safe Schema for returning User data to clients (Output)
class UserResponse(UserBase):
    id: int
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime
    status: Optional[str] = None
    auth_provider: Optional[str] = None
    must_change_password: Optional[bool] = None
    hris_id: Optional[str] = None
    facility_id: Optional[str] = None
    lab_id: Optional[str] = None
    mobile: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    division_id: Optional[str] = None
    district_id: Optional[str] = None
    upazila_id: Optional[str] = None
    union_id: Optional[str] = None

    # Pydantic v2 configuration to read data from SQLAlchemy ORM objects
    model_config = ConfigDict(from_attributes=True)