import pytest

from src.schemas.tasks import TaskStatus


# ---------- CREATE TASK ----------

@pytest.mark.asyncio
async def test_create_task_route(client, auth_headers, other_user, team_with_member):
    response = await client.post(
        "/tasks/",
        headers=auth_headers,
        json={
            "title": "Task",
            "description": "Desc",
            "deadline": None,
            "executor_ids": [other_user.id]
        }
    )

    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "Task"
    assert body["status"] == "open"
    assert other_user.id in [executor["id"] for executor in body["executors"]]

@pytest.mark.asyncio
async def test_create_task_without_team(client, auth_headers):
    response = await client.post(
        "/tasks/",
        headers=auth_headers,
        json={
            "title": "Task",
            "description": "Desc",
            "deadline": None,
            "executor_ids": []
        }
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_create_task_unauthorized(client):
    response = await client.post(
        "/tasks/",
        json={}
    )
    assert response.status_code == 401


# ---------- GET TASKS ----------

@pytest.mark.asyncio
async def test_get_my_tasks_route(client, task_with_executor, auth_headers_other):
    response = await client.get(
        "/tasks/",
        headers=auth_headers_other
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_get_created_tasks_route(client, task, auth_headers):
    response = await client.get(
        "/tasks/created",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_get_task_route(client, task, auth_headers):
    response = await client.get(
        f"/tasks/{task.id}",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["id"] == task.id


# ---------- UPDATE TASK ----------

@pytest.mark.asyncio
async def test_update_task_route(client, task, auth_headers):
    response = await client.patch(
        f"/tasks/{task.id}",
        headers=auth_headers,
        json={"title": "Updated"}
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Updated"


# ---------- UPDATE STATUS ----------

@pytest.mark.asyncio
async def test_update_task_status_route(client, task_with_executor, auth_headers_other):
    response = await client.patch(
        f"/tasks/{task_with_executor.id}/status",
        json={"status": TaskStatus.in_progress.value},
        headers=auth_headers_other
    )

    assert response.status_code == 200
    assert response.json()["status"] == "in_progress"


# ---------- DELETE TASK ----------

@pytest.mark.asyncio
async def test_delete_task_route(client, task, auth_headers):
    response = await client.delete(
        f"/tasks/{task.id}",
        headers=auth_headers
    )

    assert response.status_code == 204
