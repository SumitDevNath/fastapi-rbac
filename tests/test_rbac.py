import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import get_password_hash
from app.db.models import User, UserRole


@pytest.mark.asyncio
async def test_rbac_user_management(client: AsyncClient, db_session: AsyncSession, create_token):
    # 1. Create an Admin and a Viewer directly in the test database
    admin_user = User(
        email="admin_rbac@example.com",
        password_hash=get_password_hash("Pass123!"),
        role=UserRole.ADMIN,
        is_active=True
    )
    viewer_user = User(
        email="viewer_rbac@example.com",
        password_hash=get_password_hash("Pass123!"),
        role=UserRole.VIEWER,
        is_active=True
    )
    db_session.add_all([admin_user, viewer_user])
    await db_session.commit()
    await db_session.refresh(admin_user)
    await db_session.refresh(viewer_user)

    admin_token = create_token(admin_user.id, UserRole.ADMIN)
    viewer_token = create_token(viewer_user.id, UserRole.VIEWER)

    # 2. Viewer attempts to access GET /users (Should get 403 Forbidden)
    viewer_res = await client.get(
        "/api/v1/users",
        headers={"Authorization": f"Bearer {viewer_token}"}
    )
    assert viewer_res.status_code == 403
    assert viewer_res.json()["error"]["code"] == "FORBIDDEN"

    # 3. Admin attempts to access GET /users (Should get 200 OK)
    admin_res = await client.get(
        "/api/v1/users",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert admin_res.status_code == 200
    assert len(admin_res.json()) >= 2