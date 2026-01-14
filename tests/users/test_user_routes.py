import pytest


@pytest.mark.asyncio
async def test_get_my_profile(client, auth_headers):
    response = await client.get("/users/my_profile", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["email"] == "user@test.com"


@pytest.mark.asyncio
async def test_update_my_profile(client, auth_headers):
    response = await client.patch(
        "/users/my_profile",
        headers=auth_headers,
        json={"full_name": "Updated Name"}
    )

    assert response.status_code == 200
    assert response.json()["full_name"] == "Updated Name"


@pytest.mark.asyncio
async def test_delete_my_profile(client, auth_headers):
    response = await client.delete(
        "/users/my_profile",
        headers=auth_headers
    )
    assert response.status_code == 204
