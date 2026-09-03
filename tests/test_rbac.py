# tests/test_rbac.py
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User, UserRole
from app.core.security import get_password_hash

@pytest.mark.asyncio
async def test_rbac_enforcement(client: AsyncClient, db_session: AsyncSession, create_token):
    # 1. Create a standard USER and an EDITOR in the test database
    standard_user = User(
        email="standard_rbac@example.com",
        password_hash=get_password_hash("Pass123!"),
        role=UserRole.USER,  # The new role we added
        is_active=True
    )
    editor_user = User(
        email="editor_rbac@example.com",
        password_hash=get_password_hash("Pass123!"),
        role=UserRole.EDITOR,
        is_active=True
    )
    db_session.add_all([standard_user, editor_user])
    await db_session.commit()
    await db_session.refresh(standard_user)
    await db_session.refresh(editor_user)

    # 2. Generate tokens for both
    user_token = create_token(standard_user.id, UserRole.USER)
    editor_token = create_token(editor_user.id, UserRole.EDITOR)

    # 3. Standard USER attempts to create a project (Expect 403 Forbidden)
    # The USER role only has PROJECT_READ permissions, not PROJECT_CREATE.
    user_res = await client.post(
        "/api/v1/projects",
        json={"title": "Hacked Project", "description": "Should fail"},
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert user_res.status_code == 403
    assert user_res.json()["error"]["code"] == "FORBIDDEN"

    # 4. EDITOR attempts to create a project (Expect 201 Created)
    # The EDITOR role has PROJECT_CREATE permissions.
    editor_res = await client.post(
        "/api/v1/projects",
        json={"title": "Valid Project", "description": "Should succeed"},
        headers={"Authorization": f"Bearer {editor_token}"}
    )
    assert editor_res.status_code == 201
    assert editor_res.json()["title"] == "Valid Project"