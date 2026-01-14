import pytest

from src.services.auth_service import AuthService
from src.schemas.auth import LoginInput
from src.services.exceptions import UnauthorizedError


@pytest.mark.asyncio
async def test_login_success(session, user):
    data = LoginInput(email=user.email, password="password123")

    tokens = await AuthService.login(session, data)

    assert "access_token" in tokens
    assert "refresh_token" in tokens


@pytest.mark.asyncio
async def test_login_wrong_password(session, user):
    data = LoginInput(email=user.email, password="wrongpass")

    with pytest.raises(UnauthorizedError):
        await AuthService.login(session, data)
