from typing import Optional
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.db.database import get_db
from app.db.models import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import TokenData

# HTTPBearer automatically inspects the Authorization header for "Bearer <token>"
security_bearer = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_bearer),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Reusable FastAPI dependency that:
    1. Extracts the Bearer token from the Authorization header.
    2. Decodes and verifies the JWT signature and expiration.
    3. Looks up the user in the database.
    4. Confirms the user account is active.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # 1. Ensure the Authorization Bearer header was provided
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Bearer authentication token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials

    # 2. Decode and verify JWT token
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        user_id_str: Optional[str] = payload.get("sub")
        role: Optional[str] = payload.get("role")

        if user_id_str is None:
            raise credentials_exception

        token_data = TokenData(user_id=int(user_id_str), role=role)

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token has expired. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except (jwt.InvalidTokenError, ValueError):
        raise credentials_exception

    # 3. Look up user in SQLite
    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(token_data.user_id)

    if user is None:
        raise credentials_exception

    # 4. Enforce account activation status
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated."
        )

    return user