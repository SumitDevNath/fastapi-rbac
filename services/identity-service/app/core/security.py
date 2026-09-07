import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any

from pathlib import Path
from uuid import uuid4
import jwt
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

from app.core.config import settings

from uuid import uuid4

import jwt

def load_private_key() -> str:
    return Path(
        settings.JWT_PRIVATE_KEY_PATH
    ).read_text(
        encoding="utf-8"
    )


PRIVATE_KEY = load_private_key()


password_hash_engine = PasswordHash(
    (
        Argon2Hasher(
            time_cost=3,
            memory_cost=65536,
            parallelism=4,
        ),
    )
)


def hash_password(password: str) -> str:
    return password_hash_engine.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return password_hash_engine.verify(
        plain_password,
        hashed_password,
    )


def create_access_token(
    *,
    subject: int | str,
    role: str,
    expires_delta: timedelta | None = None,
) -> str:

    now = datetime.now(timezone.utc)

    expires_at = (
        now + expires_delta
        if expires_delta
        else now
        + timedelta(
            minutes=(
                settings
                .ACCESS_TOKEN_EXPIRE_MINUTES
            )
        )
    )

    payload = {
        "iss": settings.JWT_ISSUER,
        "aud": settings.JWT_AUDIENCE,
        "sub": str(subject),
        "role": role,
        "iat": now,
        "exp": expires_at,
        "jti": str(uuid4()),
    }

    headers = {
        "kid": settings.JWT_ACTIVE_KID,
        "typ": "JWT",
    }

    return jwt.encode(
        payload,
        PRIVATE_KEY,
        algorithm="RS256",
        headers=headers,
    )

def generate_refresh_token() -> tuple[str, str]:

    raw_token = secrets.token_urlsafe(32)

    token_hash = hashlib.sha256(
        raw_token.encode("utf-8")
    ).hexdigest()

    return raw_token, token_hash


def hash_refresh_token(raw_token: str) -> str:
    return hashlib.sha256(
        raw_token.encode("utf-8")
    ).hexdigest()