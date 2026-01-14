import pytest

from src.services.user_service import UserService
from src.schemas.users import UserCreateSchema, UserUpdateSchema
from src.services.exceptions import ConflictError, NotFoundError


@pytest.mark.asyncio
async def test_create_user_success(session):
    data = UserCreateSchema(
        email="new@test.com",
        full_name="New User",
        password="secret123"
    )

    user = await UserService.create_user(session, data)

    assert user.id is not None
    assert user.email == "new@test.com"
    assert user.password != "secret123"


@pytest.mark.asyncio
async def test_create_user_email_conflict(session, user):
    data = UserCreateSchema(
        email=user.email,
        full_name="Dup",
        password="password123"
    )

    with pytest.raises(ConflictError):
        await UserService.create_user(session, data)


@pytest.mark.asyncio
async def test_get_by_id_not_found(session):
    with pytest.raises(NotFoundError):
        await UserService.get_by_id(session, 999)


@pytest.mark.asyncio
async def test_update_profile_email(session, user):
    data = UserUpdateSchema(email="updated@test.com")

    updated = await UserService.update_profile(session, user, data)

    assert updated.email == "updated@test.com"


@pytest.mark.asyncio
async def test_delete_user(session, user):
    await UserService.delete_user(session, user)

    with pytest.raises(NotFoundError):
        await UserService.get_by_id(session, user.id)
