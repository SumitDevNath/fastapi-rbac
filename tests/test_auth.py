# tests/test_auth.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_user_creation_and_mass_assignment_protection(client: AsyncClient):
    """Verifies user creation and confirms role cannot be escalated to ADMIN."""
    response = await client.post(
        "/api/v1/users",
        json={
            "username": "alice",
            "email": "alice@example.com",
            "password": "Password123!",
            "role": "ADMIN"  # Attempted privilege escalation
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "alice@example.com"
    assert data["role"] == "user"  # Coerced to standard user


@pytest.mark.asyncio
async def test_login_issues_access_and_refresh_tokens(client: AsyncClient):
    """Verifies that login returns the exact nested schema with both tokens."""
    # 1. Create user
    await client.post(
        "/api/v1/users",
        json={"username": "bob", "email": "bob@example.com", "password": "Password123!"}
    )

    # 2. Login
    login_res = await client.post(
        "/api/v1/auth/login",
        json={"email": "bob@example.com", "password": "Password123!"}
    )
    assert login_res.status_code == 200
    data = login_res.json()
    assert "user" in data
    assert "tokens" in data
    assert data["tokens"]["token_type"] == "bearer"
    assert len(data["tokens"]["access_token"]) > 20
    assert len(data["tokens"]["refresh_token"]) > 20


@pytest.mark.asyncio
async def test_access_token_authorizes_protected_routes(client: AsyncClient):
    """Verifies access token authorizes requests to /validate and /users/me."""
    await client.post(
        "/api/v1/users",
        json={"username": "charlie", "email": "charlie@example.com", "password": "Password123!"}
    )
    login_res = await client.post(
        "/api/v1/auth/login",
        json={"email": "charlie@example.com", "password": "Password123!"}
    )
    access_token = login_res.json()["tokens"]["access_token"]

    # Validate route
    val_res = await client.get(
        "/api/v1/auth/validate",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert val_res.status_code == 200
    assert val_res.json()["email"] == "charlie@example.com"

    # Profile route
    me_res = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert me_res.status_code == 200
    assert me_res.json()["email"] == "charlie@example.com"


@pytest.mark.asyncio
async def test_refresh_token_rotation_success(client: AsyncClient):
    """Verifies refresh token can be exchanged for a new pair (Rotation)."""
    await client.post(
        "/api/v1/users",
        json={"username": "david", "email": "david@example.com", "password": "Password123!"}
    )
    login_res = await client.post(
        "/api/v1/auth/login",
        json={"email": "david@example.com", "password": "Password123!"}
    )
    old_refresh = login_res.json()["tokens"]["refresh_token"]

    refresh_res = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": old_refresh}
    )
    assert refresh_res.status_code == 200
    new_tokens = refresh_res.json()
    assert new_tokens["refresh_token"] != old_refresh
    assert "access_token" in new_tokens


@pytest.mark.asyncio
async def test_token_reuse_detection_terminates_all_sessions(client: AsyncClient):
    """Verifies replaying an already-consumed refresh token triggers mass revocation."""
    await client.post(
        "/api/v1/users",
        json={"username": "eve", "email": "eve@example.com", "password": "Password123!"}
    )
    login_res = await client.post(
        "/api/v1/auth/login",
        json={"email": "eve@example.com", "password": "Password123!"}
    )
    initial_refresh = login_res.json()["tokens"]["refresh_token"]

    # 1. Legitimate refresh consumes the token
    rotate_res = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": initial_refresh}
    )
    assert rotate_res.status_code == 200
    new_refresh = rotate_res.json()["refresh_token"]

    # 2. Attacker replays initial_refresh -> Triggers reuse detection
    reuse_res = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": initial_refresh}
    )
    assert reuse_res.status_code == 401

    # 3. Legitimate user tries to use new_refresh -> Must now also fail because sessions were wiped
    subsequent_res = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": new_refresh}
    )
    assert subsequent_res.status_code == 401


@pytest.mark.asyncio
async def test_logout_revokes_token(client: AsyncClient):
    """Verifies that logout revokes the token so it cannot be used again."""
    await client.post(
        "/api/v1/users",
        json={"username": "frank", "email": "frank@example.com", "password": "Password123!"}
    )
    login_res = await client.post(
        "/api/v1/auth/login",
        json={"email": "frank@example.com", "password": "Password123!"}
    )
    refresh_token = login_res.json()["tokens"]["refresh_token"]

    # Logout
    logout_res = await client.post(
        "/api/v1/auth/logout",
        json={"refresh_token": refresh_token}
    )
    assert logout_res.status_code == 200
    assert logout_res.json() == {"message": "Successfully logged out."}

    # Attempt refresh with logged out token
    refresh_attempt = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token}
    )
    assert refresh_attempt.status_code == 401