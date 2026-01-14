import pytest


@pytest.mark.asyncio
async def test_create_team_route(client, auth_headers):
    response = await client.post(
        "/teams/",
        headers=auth_headers,
        json={"name": "Team"}
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Team"


@pytest.mark.asyncio
async def test_create_team_unauthorized(client):
    response = await client.post(
        "/teams/",
        json={"name": "Team"}
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_team_when_already_in_team(client, auth_headers, team):
    response = await client.post(
        "/teams/",
        headers=auth_headers,
        json={"name": "Another"}
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_team_route(client, auth_headers, team):
    response = await client.get(
        f"/teams/{team.id}",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["id"] == str(team.id)


@pytest.mark.asyncio
async def test_get_team_not_member(client, auth_headers_other, team):
    response = await client.get(
        f"/teams/{team.id}",
        headers=auth_headers_other
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_add_and_get_members_route(client, other_user, auth_headers, team):
    add = await client.post(
        f"/teams/{team.id}/members/{other_user.id}",
        headers=auth_headers
    )
    assert add.status_code == 200

    members = await client.get(
        f"/teams/{team.id}/members",
        headers=auth_headers
    )
    assert members.status_code == 200
    assert len(members.json()) == 2


@pytest.mark.asyncio
async def test_promote_and_demote_route(client, other_user, auth_headers, team_with_member):
    promote = await client.post(
        f"/teams/{team_with_member.id}/promote/{other_user.id}",
        headers=auth_headers
    )
    assert promote.status_code == 200

    demote = await client.post(
        f"/teams/{team_with_member.id}/demote/{other_user.id}",
        headers=auth_headers
    )
    assert demote.status_code == 200


@pytest.mark.asyncio
async def test_remove_user_route(client, other_user, auth_headers, team_with_member):
    response = await client.delete(
        f"/teams/{team_with_member.id}/members/{other_user.id}",
        headers=auth_headers
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_admin_cannot_remove_self_route(client, user, auth_headers, team):
    response = await client.delete(
        f"/teams/{team.id}/members/{user.id}",
        headers=auth_headers
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_delete_team_route(client, user, other_user, auth_headers, team_with_member):
    response = await client.delete(
        f"/teams/{team_with_member.id}",
        headers=auth_headers
    )

    assert response.status_code == 204

    assert user.team_id is None
    assert other_user.team_id is None
    assert user.role.name == "user"
