from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.tasks import Task, TaskExecutor, TaskStatus, TaskComment
from src.models.users import User, UserRole
from src.schemas.tasks import TaskCreateSchema, TaskUpdateSchema
from src.services.exceptions import ConflictError, ForbiddenError
from src.services.utils import safe_commit, get_object_or_404


class TaskService:

    @staticmethod
    async def get_task(session: AsyncSession, user: User, task_id: int) -> Task:
        stmt = (
            select(Task)
            .where(Task.id == task_id)
            .options(
                selectinload(Task.executors),  # Подгружаем с задачей её исполнителей
                selectinload(Task.evaluations),  # Подгружаем оценки, связанные с задачей
            )
        )

        result = await session.execute(stmt)
        task = result.scalar_one_or_none()

        if user.team_id != task.team_id:
            raise ForbiddenError("Нет доступа к этой задаче")
        if user.role in (UserRole.admin, UserRole.manager) or user.id in [u.id for u in task.executors] or user.id == task.creator_id:
            return task
        raise ForbiddenError("Нет доступа к этой задаче")

    @staticmethod
    async def assign_executors(session: AsyncSession, task: Task, executor_ids: list[int], current_user: User):
        """
        Проверяет каждого пользователя из списка, можно ли назначить его исполнителем задачи.
        Назначет всех пользователей из списка исполнителями, если это возможно.
        Если хотя бы один пользователь не может быть исполнителем, то функция вернёт ошибку.
        """
        executors = await session.scalars(select(User).where(User.id.in_(executor_ids)))
        executors = list(executors)

        for executor in executors:
            if executor.team_id != task.team_id:
                raise ConflictError("Исполнитель должен быть из той же команды")
            if current_user.role == UserRole.admin:
                pass
            elif current_user.role == UserRole.manager and executor.role == UserRole.employee:
                pass
            else:
                raise ForbiddenError(f"Вы не можете назначить этого пользователя {executor.id} исполнителем")
            session.add(TaskExecutor(task_id=task.id, executor_id=executor.id))

        await safe_commit(session)

    @staticmethod
    async def create_task(session: AsyncSession, user: User, data: TaskCreateSchema) -> Task:
        if not user.team_id:
            raise ConflictError("Вы не состоите в команде")
        if user.role not in (UserRole.admin, UserRole.manager):
            raise ForbiddenError("Вы не можете создать задачу")

        task = Task(
            title=data.title,
            description=data.description,
            deadline=data.deadline,
            creator_id=user.id,
            team_id=user.team_id
        )
        session.add(task)
        await session.flush()

        if data.executor_ids:
            await TaskService.assign_executors(session, task, data.executor_ids, user)

        await safe_commit(session)
        await session.refresh(task, attribute_names=['executors'])
        return task

    @staticmethod
    async def get_my_tasks(session: AsyncSession, user: User) -> list[Task]:
        await session.refresh(user, ['my_tasks'])
        return user.my_tasks

    @staticmethod
    async def get_created_tasks(session: AsyncSession, user: User) -> list[Task]:
        if user.role not in (UserRole.admin, UserRole.manager):
            raise ForbiddenError("Вы не можете создавать задачи")
        await session.refresh(user, ['created_tasks'])
        return user.created_tasks

    @staticmethod
    async def update_task(session: AsyncSession, user: User, task_id: int, data: TaskUpdateSchema) -> Task:
        task = await TaskService.get_task(session, user, task_id)
        if task.creator_id != user.id:
            raise ForbiddenError("Редактировать задачу может только её создатель")

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if field != "executor_ids" and getattr(task, field) != value:
                setattr(task, field, value)

        if data.executor_ids is not None:
            task.executors.clear()
            await session.flush()
            await TaskService.assign_executors(session, task, data.executor_ids, user)

        await safe_commit(session)
        return task

    @staticmethod
    async def update_status(session: AsyncSession, user: User, task_id: int, status: TaskStatus) -> Task:
        task = await TaskService.get_task(session, user, task_id)
        executor_ids = {u.id for u in task.executors}
        if user.id not in executor_ids:
            raise ForbiddenError("Вы не можете менять статус этой задачи")
        if task.evaluations and len(task.evaluations) > 0:
            raise ConflictError("Задача уже оценена")
        task.status = status
        await safe_commit(session)
        return task

    @staticmethod
    async def delete_task(session: AsyncSession, user: User, task_id: int):
        task = await TaskService.get_task(session, user, task_id)
        if task.creator_id != user.id:
            raise ForbiddenError("Удалять задачу может только её создатель")
        await session.delete(task)
        await safe_commit(session)

    @staticmethod
    async def create_comment(session: AsyncSession, user: User, task_id: int, message: str) -> TaskComment:
        task = await TaskService.get_task(session, user, task_id)
        if user.id not in [task.creator_id] + [u.id for u in task.executors]:
            raise ForbiddenError("Вы не можете оставлять комментарии к этой задаче")

        comment = TaskComment(task_id=task_id, author_id=user.id, message=message)
        session.add(comment)
        await safe_commit(session)
        await session.refresh(comment)
        return comment

    @staticmethod
    async def get_comments(session: AsyncSession, user: User, task_id: int) -> list[TaskComment]:
        task = await TaskService.get_task(session, user, task_id)
        await session.refresh(task, ["comments"])
        return task.comments

    @staticmethod
    async def delete_comment(session: AsyncSession, user: User, task_id: int, comment_id: int):
        comment = await get_object_or_404(session, TaskComment, comment_id)
        if comment.task_id != task_id:
            raise ConflictError("Комментарий не относится к этой задаче")
        if comment.author_id != user.id:
            raise ForbiddenError("Можно удалять только свои комментарии")
        await session.delete(comment)
        await safe_commit(session)
