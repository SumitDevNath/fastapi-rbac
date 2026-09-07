import base64
from pathlib import Path

from cryptography.hazmat.primitives import (
    serialization,
)
from cryptography.hazmat.primitives.asymmetric.rsa import (
    RSAPublicKey,
)

from app.core.config import settings


def _base64url_uint(value: int) -> str:
    raw = value.to_bytes(
        (value.bit_length() + 7) // 8,
        byteorder="big",
    )

    return (
        base64.urlsafe_b64encode(raw)
        .rstrip(b"=")
        .decode("ascii")
    )


def public_key_to_jwk(
    *,
    public_key: RSAPublicKey,
    kid: str,
) -> dict:

    numbers = public_key.public_numbers()

    return {
        "kty": "RSA",
        "kid": kid,
        "use": "sig",
        "alg": "RS256",
        "n": _base64url_uint(numbers.n),
        "e": _base64url_uint(numbers.e),
    }


def load_jwks() -> dict:

    keys = []

    public_dir = Path(
        settings.JWT_PUBLIC_KEYS_DIR
    )

    for pem_path in sorted(
        public_dir.glob("*.pem")
    ):

        public_key = serialization.load_pem_public_key(
            pem_path.read_bytes()
        )

        if not isinstance(
            public_key,
            RSAPublicKey,
        ):
            continue

        keys.append(
            public_key_to_jwk(
                public_key=public_key,
                kid=pem_path.stem,
            )
        )

    return {
        "keys": keys
    }