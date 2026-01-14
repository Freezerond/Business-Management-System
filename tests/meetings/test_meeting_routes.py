import pytest
import datetime

from src.services.jwt_manager import create_access_token


# -------------------- CREATE MEETING --------------------

@pytest.mark.asyncio
async def test_create_meeting_route(client, auth_headers, other_user, team_with_member, time_slot):
    start, end = time_slot
    response = await client.post(
        "/meetings/",
        headers=auth_headers,
        json={
            "title": "Planning",
            "description": "Sprint planning",
            "start_time": start.isoformat(),
            "end_time": end.isoformat(),
            "participant_ids": [other_user.id],
        },
    )

    assert response.status_code == 201
    body = response.json()

    assert body["title"] == "Planning"
    assert other_user.id in [participant["id"] for participant in body["participants"]]


@pytest.mark.asyncio
async def test_create_meeting_unauthorized(client):
    response = await client.post("/meetings/", json={})
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_meeting_by_employee_forbidden(client, other_user, team_with_member, time_slot):
    token = create_access_token(
        {"sub": str(other_user.id), "role": other_user.role.value}
    )
    headers = {"Authorization": f"Bearer {token}"}

    start, end = time_slot
    response = await client.post(
        "/meetings/",
        headers=headers,
        json={
            "title": "Hack",
            "description": "Try create",
            "start_time": start.isoformat(),
            "end_time": end.isoformat(),
            "participant_ids": [],
        },
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_create_meeting_with_invalid_time(client, auth_headers, team):
    start = datetime.datetime.utcnow() + datetime.timedelta(days=1)
    end = start - datetime.timedelta(hours=1)

    response = await client.post(
        "/meetings/",
        headers=auth_headers,
        json={
            "title": "Invalid",
            "description": "Wrong time",
            "start_time": start.isoformat(),
            "end_time": end.isoformat(),
            "participant_ids": [],
        },
    )

    assert response.status_code == 400


# -------------------- GET MY MEETINGS --------------------

@pytest.mark.asyncio
async def test_get_my_meetings_route(client, auth_headers, other_user, team_with_member, time_slot):
    start, end = time_slot

    await client.post(
        "/meetings/",
        headers=auth_headers,
        json={
            "title": "Planning",
            "description": "Sprint planning",
            "start_time": start.isoformat(),
            "end_time": end.isoformat(),
            "participant_ids": [other_user.id],
        },
    )

    response = await client.get("/meetings/", headers=auth_headers)

    assert response.status_code == 200
    assert len(response.json()) == 1


# -------------------- GET MEETING --------------------

@pytest.mark.asyncio
async def test_get_meeting_route(client, auth_headers, other_user, team_with_member, time_slot):
    start, end = time_slot

    create = await client.post(
        "/meetings/",
        headers=auth_headers,
        json={
            "title": "Planning",
            "description": "Sprint planning",
            "start_time": start.isoformat(),
            "end_time": end.isoformat(),
            "participant_ids": [other_user.id],
        },
    )

    meeting_id = create.json()["id"]

    response = await client.get(f"/meetings/{meeting_id}", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["id"] == meeting_id


@pytest.mark.asyncio
async def test_get_meeting_not_participant_forbidden(client, auth_headers, other_user, team_with_member, time_slot):
    start, end = time_slot

    create = await client.post(
        "/meetings/",
        headers=auth_headers,
        json={
            "title": "Private",
            "description": "Secret",
            "start_time": start.isoformat(),
            "end_time": end.isoformat(),
            "participant_ids": [],
        },
    )

    meeting_id = create.json()["id"]

    token_other = create_access_token(
        {"sub": str(other_user.id), "role": other_user.role.value}
    )
    headers_other = {"Authorization": f"Bearer {token_other}"}

    response = await client.get(f"/meetings/{meeting_id}", headers=headers_other)

    assert response.status_code == 403


# -------------------- DELETE MEETING --------------------

@pytest.mark.asyncio
async def test_delete_meeting_by_creator(client, auth_headers, other_user, team_with_member, time_slot):
    start, end = time_slot

    create = await client.post(
        "/meetings/",
        headers=auth_headers,
        json={
            "title": "Planning",
            "description": "Sprint planning",
            "start_time": start.isoformat(),
            "end_time": end.isoformat(),
            "participant_ids": [other_user.id],
        },
    )

    meeting_id = create.json()["id"]

    response = await client.delete(
        f"/meetings/{meeting_id}",
        headers=auth_headers,
    )

    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_meeting_by_non_creator_forbidden(client, user, other_user, team_with_member, time_slot):
    start, end = time_slot

    create = await client.post(
        "/meetings/",
        headers={"Authorization": f"Bearer {create_access_token({'sub': str(user.id), 'role': user.role.value})}"},
        json={
            "title": "Planning",
            "description": "Sprint planning",
            "start_time": start.isoformat(),
            "end_time": end.isoformat(),
            "participant_ids": [],
        },
    )

    meeting_id = create.json()["id"]

    token_other = create_access_token(
        {"sub": str(other_user.id), "role": other_user.role.value}
    )
    headers_other = {"Authorization": f"Bearer {token_other}"}

    response = await client.delete(
        f"/meetings/{meeting_id}",
        headers=headers_other,
    )

    assert response.status_code == 403
