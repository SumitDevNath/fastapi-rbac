import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import get_password_hash
from app.db.models import User, UserRole


@pytest.mark.asyncio
async def test_project_crud_lifecycle(client: AsyncClient, db_session: AsyncSession, create_token):
    # 1. Seed Editor & Manager users
    editor = User(
        email="editor_crud@example.com",
        password_hash=get_password_hash("Pass123!"),
        role=UserRole.EDITOR,
        is_active=True
    )
    manager = User(
        email="manager_crud@example.com",
        password_hash=get_password_hash("Pass123!"),
        role=UserRole.MANAGER,
        is_active=True
    )
    db_session.add_all([editor, manager])
    await db_session.commit()
    await db_session.refresh(editor)
    await db_session.refresh(manager)

    editor_token = create_token(editor.id, UserRole.EDITOR)
    manager_token = create_token(manager.id, UserRole.MANAGER)

    # 2. Editor creates a project (POST /projects) -> 201 Created
    create_res = await client.post(
        "/api/v1/projects",
        json={"title": "Cloud Infrastructure", "description": "AWS Setup"},
        headers={"Authorization": f"Bearer {editor_token}"}
    )
    assert create_res.status_code == 201
    project_id = create_res.json()["id"]
    assert create_res.json()["title"] == "Cloud Infrastructure"

    # 3. Editor attempts to delete the project (DELETE /projects/{id}) -> 403 Forbidden
    delete_editor_res = await client.delete(
        f"/api/v1/projects/{project_id}",
        headers={"Authorization": f"Bearer {editor_token}"}
    )
    assert delete_editor_res.status_code == 403

    # 4. Manager deletes the project (DELETE /projects/{id}) -> 204 No Content
    delete_manager_res = await client.delete(
        f"/api/v1/projects/{project_id}",
        headers={"Authorization": f"Bearer {manager_token}"}
    )
    assert delete_manager_res.status_code == 204

    # 5. Querying the deleted project should now return 404 Not Found
    get_res = await client.get(
        f"/api/v1/projects/{project_id}",
        headers={"Authorization": f"Bearer {manager_token}"}
    )
    assert get_res.status_code == 404
    assert get_res.json()["error"]["code"] == "RESOURCE_NOT_FOUND"