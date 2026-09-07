import httpx
import jwt

from fastapi import (
    Depends,
    HTTPException,
    status,
)
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from app.core.config import settings
from app.core.jwks_client import jwks_client
from app.schemas.principal import (
    AuthenticatedPrincipal,
)


bearer_scheme = HTTPBearer(
    auto_error=False
)


async def get_current_principal(
    credentials:
        HTTPAuthorizationCredentials
        | None = Depends(bearer_scheme),
) -> AuthenticatedPrincipal:

    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required.",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    token = credentials.credentials

    try:
        header = jwt.get_unverified_header(
            token
        )

        if header.get("alg") != "RS256":
            raise jwt.InvalidAlgorithmError(
                "Unexpected JWT algorithm."
            )

        kid = header.get("kid")

        if not kid:
            raise jwt.InvalidTokenError(
                "Missing JWT kid."
            )

        public_key = await jwks_client.get_key(
            kid
        )

        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            issuer=settings.JWT_ISSUER,
            audience=settings.JWT_AUDIENCE,
            options={
                "require": [
                    "iss",
                    "aud",
                    "sub",
                    "role",
                    "iat",
                    "exp",
                    "jti",
                ]
            },
        )

        return AuthenticatedPrincipal(
            identity_id=int(
                payload["sub"]
            ),
            role=str(
                payload["role"]
            ),
            jti=str(
                payload["jti"]
            ),
        )

    except (
        jwt.InvalidTokenError,
        ValueError,
        RuntimeError,
        httpx.HTTPError,
    ) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=(
                "Invalid or expired "
                "access token."
            ),
            headers={
                "WWW-Authenticate": "Bearer"
            },
        ) from exc