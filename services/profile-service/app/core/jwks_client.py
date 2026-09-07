import asyncio

import httpx
import jwt

from app.core.config import settings


class JWKSClient:
    def __init__(self):
        self._keys: dict[str, object] = {}
        self._lock = asyncio.Lock()

    async def _refresh(self) -> None:
        async with httpx.AsyncClient(
            timeout=3.0
        ) as client:
            response = await client.get(
                settings.IDENTITY_JWKS_URL
            )

            response.raise_for_status()

            data = response.json()

        keys: dict[str, object] = {}

        for jwk_data in data.get(
            "keys",
            [],
        ):
            kid = jwk_data.get("kid")

            if not kid:
                continue

            py_jwk = jwt.PyJWK.from_dict(
                jwk_data
            )

            keys[kid] = py_jwk.key

        if not keys:
            raise RuntimeError(
                "Identity JWKS contains "
                "no usable keys."
            )

        self._keys = keys

    async def get_key(
        self,
        kid: str,
    ):
        existing = self._keys.get(kid)

        if existing is not None:
            return existing

        async with self._lock:
            existing = self._keys.get(kid)

            if existing is not None:
                return existing

            await self._refresh()

            key = self._keys.get(kid)

            if key is None:
                raise RuntimeError(
                    f"Unknown JWT kid: {kid}"
                )

            return key


jwks_client = JWKSClient()