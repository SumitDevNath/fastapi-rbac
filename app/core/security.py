from datetime import datetime, timedelta, timezone
import hashlib
import secrets
from typing import Any, Optional
import jwt
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from app.core.config import settings

# 1. Initialize modern Argon2id Password Hasher
# Uses OWASP-recommended minimum parameters for Argon2id
password_hash_engine = PasswordHash((
    Argon2Hasher(
        time_cost=3,          # 3 iterations
        memory_cost=65536,    # 64 MB of RAM
        parallelism=4,        # 4 parallel threads
    ),
))


def get_password_hash(password: str) -> str:
    """
    Hashes a plaintext password using Argon2id with an auto-generated random salt.
    """
    return password_hash_engine.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plaintext password against a stored Argon2id hash in constant time.
    """
    return password_hash_engine.verify(plain_password, hashed_password)


def create_access_token(
    subject: int | str,
    role: str,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Generates a cryptographically signed JWT access token.
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    # Standard RFC 7519 JWT Claims
    payload: dict[str, Any] = {
        "sub": str(subject),       # Subject (User ID)
        "role": role,              # User Role for quick authorization
        "exp": expire,             # Expiration timestamp
        "iat": datetime.now(timezone.utc),  # Issued At timestamp
    }

    encoded_jwt = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt

def generate_refresh_token() -> tuple[str, str]:
    """
    Generates a secure random refresh token and its SHA-256 hash.
    Returns: (raw_token, token_hash)
    """
    # 1. Generate 32 bytes of secure random data, URL-safe base64 encoded (43 chars)
    raw_token = secrets.token_urlsafe(32)
    
    # 2. Generate a SHA-256 hash of the token for database storage
    token_hash = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
    
    return raw_token, token_hash