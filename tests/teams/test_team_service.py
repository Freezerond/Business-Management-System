import pytest
from backend.services.team_service import TeamService
from backend.models.users import UserRole
from backend.services.exceptions import ConflictError, ForbiddenError
from backend.models.teams import Team


# -------------------- CREATE TEAM --------------------

@pytest.mark.asyncio
async def test_create_team(session, user):
    team = await TeamService.create_team(session, user, "Team A")

    assert isinstance(team, Team)
    assert team.name == "Team A"
    assert user.team_id == team.id
    assert user.role == UserRole.admin


@pytest.mark.asyncio
async def test_create_team_when_user_already_in_team(session, user, team):
    with pytest.raises(ConflictError):
        await TeamService.create_team(session, user, "Team B")


# -------------------- GET TEAM --------------------

@pytest.mark.asyncio
async def test_get_team_by_member(session, user, team):
    fetched = await TeamService.get_team(session, user, team.id)
    assert fetched.id == team.id


@pytest.mark.asyncio
async def test_get_team_by_non_member(session, user, other_user, team):
    with pytest.raises(ForbiddenError):
        await TeamService.get_team(session, other_user, team.id)


# -------------------- GET MEMBERS --------------------

@pytest.mark.asyncio
async def test_get_team_members(session, user, other_user, team_with_member):
    members = await TeamService.get_members(session, user, team_with_member.id)

    assert len(members) == 2
    assert user in members
    assert other_user in members
    assert user.role == UserRole.admin
    assert other_user.role == UserRole.employee


# -------------------- ADD USER --------------------

@pytest.mark.asyncio
async def test_add_user_by_admin(session, user, other_user, team):
    await TeamService.add_user(session, user, team.id, other_user.id)

    assert other_user.team_id == team.id
    assert other_user.role == UserRole.employee


@pytest.mark.asyncio
async def test_add_user_by_non_admin(session, user, other_user, team):
    with pytest.raises(ForbiddenError):
        await TeamService.add_user(session, other_user, team.id, user.id)


@pytest.mark.asyncio
async def test_add_user_already_in_team(session, user, other_user, team_with_member):
    with pytest.raises(ConflictError):
        await TeamService.add_user(session, user, team_with_member.id, other_user.id)


# -------------------- CHANGE ROLE --------------------

@pytest.mark.asyncio
async def test_change_role_by_admin(session, user, other_user, team_with_member):
    await TeamService.change_role(session, user, team_with_member.id, other_user.id, UserRole.manager)
    assert other_user.role == UserRole.manager


@pytest.mark.asyncio
async def test_change_role_by_non_admin(session, user, other_user, team_with_member):
    with pytest.raises(ForbiddenError):
        await TeamService.change_role(session, other_user, team_with_member.id, user.id, UserRole.manager)


# -------------------- REMOVE USER --------------------

@pytest.mark.asyncio
async def test_remove_user_by_admin(session, user, other_user, team_with_member):
    await TeamService.remove_user(session, user, team_with_member.id, other_user.id)
    assert other_user.team_id is None
    assert other_user.role == UserRole.user


@pytest.mark.asyncio
async def test_admin_cannot_remove_self(session, user, team):
    with pytest.raises(ConflictError):
        await TeamService.remove_user(session, user, team.id, user.id)


# -------------------- DELETE TEAM --------------------

@pytest.mark.asyncio
async def test_delete_team_minimal(session, user, team):
    await TeamService.delete_team(session, user, team.id)

    await session.refresh(user)
    assert user.team_id is None
    assert user.role == UserRole.user


@pytest.mark.asyncio
async def test_delete_team_resets_all_members(session, user, other_user, team_with_member):
    await TeamService.delete_team(session, user, team_with_member.id)

    await session.refresh(user)
    await session.refresh(other_user)

    assert user.team_id is None
    assert user.role == UserRole.user
    assert other_user.team_id is None
    assert other_user.role == UserRole.user
