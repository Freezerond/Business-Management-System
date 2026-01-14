import pytest


@pytest.mark.asyncio
async def test_register(client):
    response = await client.post(
        "/auth/register",
        json={
            "email": "api@test.com",
            "full_name": "API User",
            "password": "password123"
        }
    )
    assert response.status_code == 201
    assert response.json()["email"] == "api@test.com"


@pytest.mark.asyncio
async def test_login_api(client, user):
    response = await client.post(
        "/auth/login",
        data={
            "username": user.email,
            "password": "password123"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
