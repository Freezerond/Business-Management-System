import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.teams import Team
from src.models.users import User
from src.models.users import UserRole
from src.services.exceptions import ForbiddenError, ConflictError
from src.services.utils import safe_commit, get_object_or_404


class TeamService:

    @staticmethod
    def ensure_admin(user: User, team_id: uuid.UUID):
        """Проверяет, что пользователь является администратором указанной команды."""
        if user.role != UserRole.admin or user.team_id != team_id:
            raise ForbiddenError("Только администратор команды может управлять ей")

    @staticmethod
    def ensure_member(user: User, team_id: uuid.UUID):
        """Проверяет, что пользователь является членом указанной команды"""
        if user.team_id != team_id:
            raise ForbiddenError("Пользователь не является членом команды")

    @staticmethod
    async def create_team(session: AsyncSession, user: User, name: str) -> Team:
        if user.team_id is not None:
            raise ConflictError("Вы уже состоите в команде")

        team = Team(name=name)
        session.add(team)
        await session.flush()

        user.team_id = team.id
        user.role = UserRole.admin

        await safe_commit(session)
        await session.refresh(team)
        return team

    @staticmethod
    async def get_team(session: AsyncSession, user: User, team_id: uuid.UUID) -> Team:
        team = await get_object_or_404(session, Team, team_id)
        TeamService.ensure_member(user, team_id)
        return team

    @staticmethod
    async def get_members(session: AsyncSession, user: User, team_id: uuid.UUID) -> list[User]:
        """Возвращает список членов команды"""
        team = await get_object_or_404(session, Team, team_id)
        TeamService.ensure_member(user, team_id)

        await session.refresh(team, ["users"])
        return team.users

    @staticmethod
    async def add_user(session: AsyncSession, admin: User, team_id: uuid.UUID, user_id: int):
        """Добавляет пользователя в команду"""
        TeamService.ensure_admin(admin, team_id)

        user = await get_object_or_404(session, User, user_id)

        if user.team_id is not None:
            raise ConflictError("Пользователь уже состоит в команде")

        user.team_id = team_id
        user.role = UserRole.employee

        await safe_commit(session)

    @staticmethod
    async def change_role(session: AsyncSession, admin: User, team_id: uuid.UUID, user_id: int, role: UserRole):
        """Изменяет должность сотрудника"""
        TeamService.ensure_admin(admin, team_id)

        if admin.id == user_id:
            raise ConflictError(f"Вы не можете изменить свою роль в команде")

        user = await get_object_or_404(session, User, user_id)
        TeamService.ensure_member(user, team_id)

        if user.role == role:
            raise ConflictError(f"Пользователь уже {role.value}")
        user.role = role

        await safe_commit(session)

    @staticmethod
    async def remove_user(session: AsyncSession, admin: User, team_id: uuid.UUID, user_id: int):
        """Удаляет сотрудника из команды, делает его снова обычным пользователем."""
        TeamService.ensure_admin(admin, team_id)

        user = await get_object_or_404(session, User, user_id)

        if user.id == admin.id:
            raise ConflictError("Администратор не может удалить себя")

        TeamService.ensure_member(user, team_id)

        user.team_id = None
        user.role = UserRole.user
        await safe_commit(session)

    @staticmethod
    async def delete_team(session: AsyncSession, admin: User, team_id: uuid.UUID):
        TeamService.ensure_admin(admin, team_id)

        team = await get_object_or_404(session, Team, team_id)

        await session.refresh(team, ["users"])
        for user in team.users:
            user.role = UserRole.user
            user.team_id = None

        await session.delete(team)
        await safe_commit(session)
