from fastapi import APIRouter, status

from src.api.core.dependencies import SessionDep, UserDep
from src.services.evaluation_service import EvaluationService
from src.schemas.evaluations import (EvaluationPublicSchema,
                                     EvaluationCreateSchema,
                                     EvaluationUpdateSchema,
                                     AvgEvaluationSchema)
from src.api.core.decorators import handle_service_errors

router = APIRouter(prefix="/evaluations", tags=["Оценки"])


@router.post("/{task_id}",
             response_model=EvaluationPublicSchema,
             status_code=status.HTTP_201_CREATED,
             summary="Оценить выполнение задачи сотрудником")
@handle_service_errors
async def create_evaluation(task_id: int, data: EvaluationCreateSchema, session: SessionDep, current_user: UserDep):
    return await EvaluationService.create_evaluation(session, current_user, task_id, data)


@router.get("/{task_id}/{executor_id}",
            response_model=EvaluationPublicSchema,
            summary="Получить оценку пользователя по выполненной задаче")
@handle_service_errors
async def get_evaluation(task_id: int, executor_id: int, session: SessionDep, current_user: UserDep):
    return await EvaluationService.get_evaluation(session, current_user, task_id, executor_id)


@router.patch("/{task_id}/{executor_id}",
              response_model=EvaluationPublicSchema,
              summary="Изменить оценку пользователя по выполненной задаче")
@handle_service_errors
async def update_evaluation(task_id: int, executor_id: int, data: EvaluationUpdateSchema, session: SessionDep, current_user: UserDep):
    return await EvaluationService.update_evaluation(session, current_user, task_id, executor_id, data)


@router.delete("/{task_id}/{executor_id}",
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Удалить оценку")
@handle_service_errors
async def delete_evaluation(task_id: int, executor_id: int, session: SessionDep, current_user: UserDep):
    await EvaluationService.delete_evaluation(session, current_user, task_id, executor_id)


@router.get("/my_given",
            response_model=list[EvaluationPublicSchema],
            summary="Получить все оценки, которые пользователь поставил")
@handle_service_errors
async def get_my_given(session: SessionDep, current_user: UserDep):
    return await EvaluationService.get_my_given(session, current_user)


@router.get("/my_received",
            response_model=list[EvaluationPublicSchema],
            summary="Получить все мои оценки")
@handle_service_errors
async def get_my_received(session: SessionDep, current_user: UserDep):
    return await EvaluationService.get_my_received(session, current_user)


@router.get("/average",
            response_model=AvgEvaluationSchema,
            summary="Получить среднюю оценку пользователя за период")
@handle_service_errors
async def get_average(session: SessionDep, current_user: UserDep, user_id: int, start: str | None = None, end: str | None = None):
    return await EvaluationService.get_average(session, current_user, user_id, start, end)
