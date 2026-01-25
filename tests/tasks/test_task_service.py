import pytest

from backend.models.tasks import Task, TaskStatus
from backend.models.users import UserRole
from backend.schemas.tasks import TaskCreateSchema, TaskUpdateSchema
from backend.services.task_service import TaskService
from backend.services.exceptions import ForbiddenError, ConflictError
from backend.services.team_service import TeamService


# ---------- CREATE TASK ----------

@pytest.mark.asyncio
async def test_create_task_by_admin(session, user, other_user, team_with_member):
    task = await TaskService.create_task(
        session,
        user,
        data=TaskCreateSchema(
            title="Task",
            description="Desc",
            deadline=None,
            executor_ids=[other_user.id],
        )
    )

    assert isinstance(task, Task)
    assert task.title == "Task"
    assert task.creator_id == user.id
    assert task.team_id == user.team_id
    assert task.status == TaskStatus.open


@pytest.mark.asyncio
async def test_create_task_without_team(session, user):
    with pytest.raises(ConflictError):
        await TaskService.create_task(
            session,
            user,
            data=TaskCreateSchema(
                title="Task",
                description="Desc",
                deadline=None,
                executor_ids=[],
            )
        )


@pytest.mark.asyncio
async def test_create_task_with_executor_not_from_team(session, user, other_user, team):
    with pytest.raises(ConflictError):
        await TaskService.create_task(
            session,
            user,
            data=TaskCreateSchema(
                title="Task",
                description="Desc",
                deadline=None,
                executor_ids=[other_user.id],
            )
        )


@pytest.mark.asyncio
async def test_create_task_by_employee_forbidden(session, user, other_user, team_with_member):
    with pytest.raises(ForbiddenError):
        await TaskService.create_task(
            session,
            other_user,
            data=TaskCreateSchema(
                title="Task",
                description="Desc",
                deadline=None,
                executor_ids=[],
            )
        )


@pytest.mark.asyncio
async def test_manager_cannot_assign_manager(session, user, other_user, team_with_member):
    await TeamService.change_role(session, user, user.team_id, other_user.id, UserRole.manager)

    with pytest.raises(ForbiddenError):
        await TaskService.create_task(
            session,
            other_user,  # manager
            TaskCreateSchema(
                title="Task",
                description="Desc",
                executor_ids=[user.id],  # admin
            )
        )


# ---------- GET TASK ----------

@pytest.mark.asyncio
async def test_get_task_by_creator(session, user, task):
    fetched = await TaskService.get_task(session, user, task.id)
    assert fetched.id == task.id


@pytest.mark.asyncio
async def test_get_task_by_executor(session, other_user, task_with_executor):
    fetched = await TaskService.get_task(session, other_user, task_with_executor.id)
    assert fetched.id == task_with_executor.id


@pytest.mark.asyncio
async def test_get_task_outsider_forbidden(session, other_user, task):
    with pytest.raises(ForbiddenError):
        await TaskService.get_task(session, other_user, task.id)


# ---------- UPDATE TASK ----------

@pytest.mark.asyncio
async def test_update_task_by_creator(session, user, task):
    updated = await TaskService.update_task(
        session,
        user,
        task.id,
        data=TaskUpdateSchema(
            title="New",
            description="New",
        )
    )

    assert updated.title == "New"
    assert updated.description == "New"


@pytest.mark.asyncio
async def test_update_task_by_non_creator_forbidden(session, other_user, task_with_executor):
    with pytest.raises(ForbiddenError):
        await TaskService.update_task(
            session,
            other_user,
            task_with_executor.id,
            data=TaskUpdateSchema(title="Hack")
        )


# ---------- UPDATE STATUS ----------

@pytest.mark.asyncio
async def test_update_status_by_executor(session, user, other_user, task_with_executor):
    updated = await TaskService.update_status(
        session,
        other_user,
        task_with_executor.id,
        TaskStatus.in_progress
    )

    assert updated.status == TaskStatus.in_progress


@pytest.mark.asyncio
async def test_update_status_by_non_executor_forbidden(session, user, task):
    with pytest.raises(ForbiddenError):
        await TaskService.update_status(
            session,
            user,
            task.id,
            TaskStatus.done
        )


# ---------- DELETE TASK ----------

@pytest.mark.asyncio
async def test_delete_task_by_creator(session, user, task_with_executor):
    await TaskService.delete_task(session, user, task_with_executor.id)
