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

        new_keys: dict[str, object] = {}

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

            new_keys[kid] = py_jwk.key

        if not new_keys:
            raise RuntimeError(
                "Identity JWKS returned "
                "no usable keys."
            )

        self._keys = new_keys

    async def get_key(
        self,
        kid: str,
    ):
        key = self._keys.get(kid)

        if key is not None:
            return key

        async with self._lock:

            key = self._keys.get(kid)

            if key is not None:
                return key

            await self._refresh()

            key = self._keys.get(kid)

            if key is None:
                raise RuntimeError(
                    f"Unknown JWT kid: {kid}"
                )

            return key


jwks_client = JWKSClient()