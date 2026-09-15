# from typing import Optional
# import jwt
# from fastapi import Depends, HTTPException, status
# from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
# from sqlalchemy.ext.asyncio import AsyncSession
# from app.core.config import settings
# from app.db.database import get_db
# from app.db.models import User
# from app.repositories.user_repository import UserRepository
# from app.schemas.auth import TokenData

# # HTTPBearer automatically inspects the Authorization header for "Bearer <token>"
# security_bearer = HTTPBearer(auto_error=False)


# async def get_current_user(
#     credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_bearer),
#     db: AsyncSession = Depends(get_db)
# ) -> User:
#     """
#     Reusable FastAPI dependency that:
#     1. Extracts the Bearer token from the Authorization header.
#     2. Decodes and verifies the JWT signature and expiration.
#     3. Looks up the user in the database.
#     4. Confirms the user account is active.
#     """
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials.",
#         headers={"WWW-Authenticate": "Bearer"},
#     )

#     # 1. Ensure the Authorization Bearer header was provided
#     if not credentials:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Missing Bearer authentication token.",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

#     token = credentials.credentials

#     # 2. Decode and verify JWT token
#     try:
#         payload = jwt.decode(
#             token,
#             settings.JWT_SECRET_KEY,
#             algorithms=[settings.JWT_ALGORITHM]
#         )
#         user_id_str: Optional[str] = payload.get("sub")
#         role: Optional[str] = payload.get("role")

#         if user_id_str is None:
#             raise credentials_exception

#         token_data = TokenData(user_id=int(user_id_str), role=role)

#     except jwt.ExpiredSignatureError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Access token has expired. Please log in again.",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     except (jwt.InvalidTokenError, ValueError):
#         raise credentials_exception

#     # 3. Look up user in SQLite
#     user_repo = UserRepository(db)
#     user = await user_repo.get_by_id(token_data.user_id)

#     if user is None:
#         raise credentials_exception

#     # 4. Enforce account activation status
#     if not user.is_active:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="User account is deactivated."
#         )

#     if user.status != "approved":
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Account pending administrator approval. Access restricted."
#         )

#     return user

from typing import Optional
import httpx
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.db.database import get_db
from app.db.models import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate

security_bearer = HTTPBearer(auto_error=False)

async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_bearer),
    db: AsyncSession = Depends(get_db)
) -> User:
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Bearer authentication token."
        )
    
    token = credentials.credentials

    # print("\n" + "="*50)
    # print(f"[1] Incoming request to protected route intercepted.")
    # print(f"[2] Token extracted (starts with): {token[:15]}...")
    # print(f"[3] Sending token to DGHS Auth Service for validation: {AUTH_VALIDATE_URL}")

    # Forward token to external DGHS Auth Service
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                settings.DGHS_AUTH_VALIDATE_URL,
                headers={"Authorization": f"Bearer {token}"},
                timeout=5.0
            )
        except httpx.RequestError as e:
            print(f"[ERROR] DGHS Auth Service is unreachable: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="External Identity Provider is unreachable."
            )

    # print(f"[4] DGHS Auth Service replied with status: HTTP {response.status_code}")

    if response.status_code != 200:
        print("[!] DGHS rejected the token. Access Denied.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token validation failed at the Identity Provider."
        )

    dghs_user_data = response.json()
    dghs_email = dghs_user_data.get("email")
    dghs_role = dghs_user_data.get("role")
    
    # print(f"[5] Token Validated! Identity confirmed as: {dghs_email} (Role: {dghs_role})")

    user_repo = UserRepository(db)
    local_user = await user_repo.get_by_email(dghs_email)
    
    if not local_user:
        # print(f"[6] Local shadow record not found. Provisioning JIT user for DB relations.")
        user_in = UserCreate(
            email=dghs_email,
            password="EXTERNAL_MANAGED_PASSWORD",
            role=dghs_role,
            status="active"
        )
        local_user = await user_repo.create(user_in)
    elif local_user.role != dghs_role:
        local_user.role = dghs_role
        await db.commit()

    # print("[7] Validation complete. Granting access to FastAPI route handler.")
    # print("="*50 + "\n")

    return local_user