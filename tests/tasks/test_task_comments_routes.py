import pytest


# ---------- CREATE COMMENT ----------

@pytest.mark.asyncio
async def test_create_comment_route(client, task, auth_headers):
    response = await client.post(
        f"/tasks/{task.id}/comments",
        headers=auth_headers,
        json={"message": "комментарий"}
    )

    assert response.status_code == 200
    assert response.json()["message"] == "комментарий"


@pytest.mark.asyncio
async def test_create_comment_unauthorized(client, task):
    response = await client.post(
        f"/tasks/{task.id}/comments",
        json={"message": "комментарий"}
    )

    assert response.status_code == 401


# ---------- GET COMMENTS ----------

@pytest.mark.asyncio
async def test_get_comments_route(client, task, auth_headers):
    await client.post(
        f"/tasks/{task.id}/comments",
        json={"message": "комментарий"},
        headers=auth_headers
    )

    response = await client.get(
        f"/tasks/{task.id}/comments",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


# ---------- DELETE COMMENT ----------

@pytest.mark.asyncio
async def test_delete_comment_route(client, task, auth_headers):
    create = await client.post(
        f"/tasks/{task.id}/comments",
        json={"message": "комментарий"},
        headers=auth_headers
    )

    comment_id = create.json()["id"]

    response = await client.delete(
        f"/tasks/{task.id}/comments/{comment_id}",
        headers=auth_headers
    )

    assert response.status_code == 204
