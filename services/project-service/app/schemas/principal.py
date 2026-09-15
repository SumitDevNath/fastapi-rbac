from pydantic import BaseModel


class AuthenticatedPrincipal(BaseModel):
    identity_id: int
    role: str
    jti: str