from pydantic import BaseModel, EmailStr, Field

from app.schemas.identity import IdentityResponse


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1)


class Tokens(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class LoginResponse(BaseModel):
    identity: IdentityResponse
    tokens: Tokens


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class LogoutRequest(BaseModel):
    refresh_token: str


class LogoutResponse(BaseModel):
    message: str