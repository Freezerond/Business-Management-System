import uuid

from fastapi import APIRouter, status

from backend.api.core.dependencies import SessionDep, UserDep
from backend.api.core.decorators import handle_service_errors
from backend.models.users import UserRole
from backend.schemas.teams import TeamCreateSchema, TeamSchema
from backend.schemas.users import UserPublicSchema
from backend.services.team_service import TeamService

router = APIRouter(prefix="/teams", tags=["Команды"])


@router.post("/",
             response_model=TeamSchema,
             status_code=status.HTTP_201_CREATED,
             summary="Создать команду")
@handle_service_errors
async def create_team(data: TeamCreateSchema, session: SessionDep, user: UserDep):
    return await TeamService.create_team(session, user, data.name)


@router.get("/{team_id}",
            response_model=TeamSchema,
            summary="Получить команду, в которой состоит пользователь")
@handle_service_errors
async def get_team(team_id: uuid.UUID, session: SessionDep, user: UserDep):
    return await TeamService.get_team(session, user, team_id)


@router.get("/{team_id}/members",
            response_model=list[UserPublicSchema],
            summary="Получить всех пользователей в команде")
@handle_service_errors
async def get_team_members(team_id: uuid.UUID, session: SessionDep, user: UserDep):
    return await TeamService.get_members(session, user, team_id)


@router.post("/{team_id}/members/{user_id}",
             summary="Добавить пользователя в команду")
@handle_service_errors
async def add_user(team_id: uuid.UUID, user_id: int, session: SessionDep, user: UserDep):
    await TeamService.add_user(session, user, team_id, user_id)
    return {"detail": "Пользователь добавлен"}


@router.post("/{team_id}/promote/{user_id}",
             summary="Повысить сотрудника до менеджера")
@handle_service_errors
async def promote_to_manager(team_id: uuid.UUID, user_id: int, session: SessionDep, user: UserDep):
    await TeamService.change_role(
        session, user, team_id, user_id, UserRole.manager
    )
    return {"detail": "Роль изменена на manager"}


@router.post("/{team_id}/demote/{user_id}",
             summary="Понизить менеджера до сотрудника")
@handle_service_errors
async def demote_to_employee(team_id: uuid.UUID, user_id: int, session: SessionDep, user: UserDep):
    await TeamService.change_role(
        session, user, team_id, user_id, UserRole.employee
    )
    return {"detail": "Роль изменена на employee"}


@router.delete("/{team_id}/members/{user_id}",
               summary="Удалить пользователя из команды")
@handle_service_errors
async def remove_user(team_id: uuid.UUID, user_id: int, session: SessionDep, user: UserDep):
    await TeamService.remove_user(session, user, team_id, user_id)
    return {"detail": "Пользователь удалён"}


@router.delete("/{team_id}",
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Удалить команду")
async def delete_team(team_id: uuid.UUID, session: SessionDep, user: UserDep):
    await TeamService.delete_team(session, user, team_id)
    return {"detail": "Команда удалена"}
