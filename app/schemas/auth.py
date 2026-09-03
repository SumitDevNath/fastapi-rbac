from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from app.schemas.user import UserResponse


# Schema for Login Request (Input)
class LoginRequest(BaseModel):
    email: EmailStr = Field(
        ...,
        description="User account email address.",
        examples=["alice@example.com"]
    )
    password: str = Field(
        ...,
        min_length=1,
        description="User plaintext password.",
        examples=["SecurePass123!"]
    )

# NEW: Represents the 'tokens' object requested by your senior
class Tokens(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

# New: Matches the exact nested Login Response body
class LoginResponse(BaseModel):
    user: UserResponse
    tokens: Tokens


# Schema for Token Response (Output)
# class TokenResponse(BaseModel):
#     access_token: str = Field(..., description="Cryptographically signed JWT bearer token.")
#     token_type: str = Field(default="bearer", description="Token type identifier.")
#     user: UserResponse = Field(..., description="Public profile of the authenticated user.")

# NEW: Request body for POST /api/v1/auth/refresh
class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(..., description="The raw refresh token string.")

# NEW: Request body for POST /api/v1/auth/logout
class LogoutRequest(BaseModel):
    refresh_token: str = Field(..., description="The raw refresh token to revoke.")

# NEW: Response body for POST /api/v1/auth/logout
class LogoutResponse(BaseModel):
    message: str


# Schema for the internal decoded JWT payload
class TokenData(BaseModel):
    user_id: Optional[int] = None
    role: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)