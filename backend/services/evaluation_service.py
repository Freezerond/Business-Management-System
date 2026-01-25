import datetime

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from backend.services.utils import get_object_or_404, safe_commit
from backend.services.exceptions import ForbiddenError, ConflictError, NotFoundError
from backend.models.evaluations import Evaluation
from backend.models.tasks import Task, TaskStatus, TaskExecutor
from backend.models.users import UserRole, User
from backend.schemas.evaluations import AvgEvaluationSchema


class EvaluationService:

    @staticmethod
    async def create_evaluation(session: AsyncSession, evaluator: User, task_id: int, data):
        task = await get_object_or_404(session, Task, task_id)

        if task.status != TaskStatus.done:
            raise ConflictError("Оценить можно только выполненную задачу")

        if evaluator.id != task.creator_id and evaluator.role != UserRole.admin:
            raise ForbiddenError("Вы не можете оценивать эту задачу")

        executor_relation = await session.scalar(
            select(TaskExecutor).where(
                TaskExecutor.task_id == task_id,
                TaskExecutor.executor_id == data.executor_id
            )
        )
        if not executor_relation:
            raise ConflictError("Этот пользователь не является исполнителем задачи")

        evaluation = Evaluation(
            task_id=task_id,
            executor_id=data.executor_id,
            evaluator_id=evaluator.id,
            score=data.score,
            comment=data.comment
        )
        session.add(evaluation)
        await safe_commit(session)
        await session.refresh(evaluation)
        return evaluation

    @staticmethod
    async def get_evaluation(session: AsyncSession, current_user: User, task_id: int, executor_id: int):
        task = await get_object_or_404(session, Task, task_id)

        evaluation = await session.scalar(
            select(Evaluation).where(
                Evaluation.task_id == task_id,
                Evaluation.executor_id == executor_id
            )
        )
        if not evaluation:
            raise NotFoundError("Оценка не найдена")

        if current_user.role != UserRole.admin and task.creator_id != current_user.id and current_user.id != executor_id:
            raise ForbiddenError("Вам недоступна эта оценка")

        return evaluation

    @staticmethod
    async def update_evaluation(session: AsyncSession, current_user: User, task_id: int, executor_id: int, data):
        evaluation = await EvaluationService.get_evaluation(session, current_user, task_id, executor_id)

        if evaluation.evaluator_id != current_user.id and current_user.role != UserRole.admin:
            raise ForbiddenError("Вы не можете изменять эту оценку")

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(evaluation, field, value)

        await safe_commit(session)
        await session.refresh(evaluation)
        return evaluation

    @staticmethod
    async def delete_evaluation(session: AsyncSession, current_user: User, task_id: int, executor_id: int):
        evaluation = await EvaluationService.get_evaluation(session, current_user, task_id, executor_id)

        if evaluation.evaluator_id != current_user.id and current_user.role != UserRole.admin:
            raise ForbiddenError("Вы не можете удалять эту оценку")

        await session.delete(evaluation)
        await safe_commit(session)

    @staticmethod
    async def get_my_given(session: AsyncSession, current_user: User):
        await session.refresh(current_user, ['evaluations_given'])
        return current_user.evaluations_given

    @staticmethod
    async def get_my_received(session: AsyncSession, current_user: User):
        await session.refresh(current_user, ['evaluations_received'])
        return current_user.evaluations_received

    @staticmethod
    async def get_average(session: AsyncSession, current_user: User, user_id: int, start: datetime.date | None, end: datetime.date | None):
        user = await get_object_or_404(session, User, user_id)

        if current_user.team_id != user.team_id:
            raise ForbiddenError("Это не ваша команда")

        if current_user.role not in (UserRole.admin, UserRole.manager) and current_user.id != user.id:
            raise ForbiddenError("У вас нет доступа к этим оценкам")

        stmt = (
            select(
                func.avg(Evaluation.score),
                func.count(Evaluation.score)
            )
            .where(
                Evaluation.executor_id == user_id,
                Evaluation.created_at >= start if start else True,
                Evaluation.created_at <= end if end else True,
            )
        )

        result = await session.execute(stmt)
        avg_score, count = result.one()
        return AvgEvaluationSchema(
            user_id=user_id,
            average_score=avg_score or 0.0,
            count=count or 0,
            start_date=start,
            end_date=end
        )
