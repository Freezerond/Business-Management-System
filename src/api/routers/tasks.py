from fastapi import APIRouter, status

from src.api.core.decorators import handle_service_errors
from src.api.core.dependencies import SessionDep, UserDep
from src.schemas.tasks import (TaskPublicSchema,
                               TaskCreateSchema,
                               TaskUpdateSchema,
                               TaskStatusUpdateSchema,
                               TaskCommentPublicSchema,
                               TaskCommentCreateSchema, TaskListPublicSchema)
from src.services.task_service import TaskService

router = APIRouter(prefix='/tasks', tags=['Задачи'])


@router.post("/",
             response_model=TaskPublicSchema,
             summary="Создать задачу")
@handle_service_errors
async def create_task(session: SessionDep, user: UserDep, data: TaskCreateSchema):
    task = await TaskService.create_task(session, user, data)
    return await TaskService.get_task(session, user, task.id)


@router.get("/",
            response_model=list[TaskListPublicSchema],
            summary="Получить мои задачи")
@handle_service_errors
async def get_my_tasks(session: SessionDep, user: UserDep):
    return await TaskService.get_my_tasks(session, user)


@router.get("/created",
            response_model=list[TaskListPublicSchema],
            summary="Получить задачи, созданные пользователем")
@handle_service_errors
async def get_created_tasks(session: SessionDep, user: UserDep):
    return await TaskService.get_created_tasks(session, user)


@router.get("/{task_id}",
            response_model=TaskPublicSchema,
            summary="Получить конкретную задачу")
@handle_service_errors
async def get_task(task_id: int, session: SessionDep, user: UserDep):
    return await TaskService.get_task(session, user, task_id)


@router.patch("/{task_id}",
              response_model=TaskPublicSchema,
              summary="Изменить задачу")
@handle_service_errors
async def update_task(task_id: int, data: TaskUpdateSchema, session: SessionDep, user: UserDep):
    return await TaskService.update_task(session, user, task_id, data)


@router.patch("/{task_id}/status",
              response_model=TaskPublicSchema,
              summary="Изменить статус задачи")
@handle_service_errors
async def update_task_status(task_id: int, data: TaskStatusUpdateSchema, session: SessionDep, user: UserDep):
    return await TaskService.update_status(session, user, task_id, data.status)


@router.delete("/{task_id}",
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Удалить задачу")
@handle_service_errors
async def delete_task(task_id: int, session: SessionDep, user: UserDep):
    await TaskService.delete_task(session, user, task_id)


@router.post("/{task_id}/comments",
             response_model=TaskCommentPublicSchema,
             summary="Оставить комментарий к задаче")
@handle_service_errors
async def create_comment(task_id: int, data: TaskCommentCreateSchema, session: SessionDep, user: UserDep):
    return await TaskService.create_comment(session, user, task_id, data.message)


@router.get("/{task_id}/comments",
            response_model=list[TaskCommentPublicSchema],
            summary="Получить все комментарии к задаче")
@handle_service_errors
async def get_comments(task_id: int, session: SessionDep, user: UserDep):
    return await TaskService.get_comments(session, user, task_id)


@router.delete("/{task_id}/comments/{comment_id}",
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Удалить комментарий к задаче")
@handle_service_errors
async def delete_comment(task_id: int, comment_id: int, session: SessionDep, user: UserDep):
    await TaskService.delete_comment(session, user, task_id, comment_id)
