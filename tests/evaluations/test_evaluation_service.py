import pytest
from src.models.tasks import TaskStatus
from src.models.evaluations import Evaluation
from src.schemas.evaluations import EvaluationCreateSchema, EvaluationUpdateSchema
from src.schemas.tasks import TaskCreateSchema
from src.services.evaluation_service import EvaluationService
from src.services.exceptions import ConflictError, ForbiddenError, NotFoundError
from src.services.task_service import TaskService


# -------------------- CREATE EVALUATION --------------------

@pytest.mark.asyncio
async def test_create_evaluation_by_creator(session, user, other_user, task_with_executor, done_task):
    eval_data = EvaluationCreateSchema(score=5, comment="Great", executor_id=other_user.id)
    evaluation = await EvaluationService.create_evaluation(session, user, task_with_executor.id, eval_data)

    assert isinstance(evaluation, Evaluation)
    assert evaluation.score == 5
    assert evaluation.comment == "Great"
    assert evaluation.executor_id == other_user.id
    assert evaluation.evaluator_id == user.id


@pytest.mark.asyncio
async def test_create_evaluation_task_not_done(session, user, other_user, task_with_executor):
    eval_data = EvaluationCreateSchema(score=4, comment="Test", executor_id=other_user.id)
    with pytest.raises(ConflictError):
        await EvaluationService.create_evaluation(session, user, task_with_executor.id, eval_data)


@pytest.mark.asyncio
async def test_create_evaluation_by_non_creator_forbidden(session, other_user, task_with_executor, done_task):
    eval_data = EvaluationCreateSchema(score=4, comment="Test", executor_id=other_user.id)
    with pytest.raises(ForbiddenError):
        await EvaluationService.create_evaluation(session, other_user, task_with_executor.id, eval_data)


@pytest.mark.asyncio
async def test_create_evaluation_for_non_executor_conflict(session, user, task_with_executor, done_task):
    eval_data = EvaluationCreateSchema(score=3, comment="Test", executor_id=user.id)
    with pytest.raises(ConflictError):
        await EvaluationService.create_evaluation(session, user, task_with_executor.id, eval_data)


# -------------------- GET EVALUATION --------------------

@pytest.mark.asyncio
async def test_get_evaluation_by_creator(session, user, other_user, task_with_executor, evaluation):
    fetched = await EvaluationService.get_evaluation(session, user, task_with_executor.id, other_user.id)
    assert fetched.task_id == evaluation.task_id
    assert fetched.executor_id == evaluation.executor_id


@pytest.mark.asyncio
async def test_get_evaluation_forbidden(session, other_user, task_with_executor, evaluation):
    with pytest.raises(ForbiddenError):
        await EvaluationService.get_evaluation(session, other_user, task_with_executor.id, other_user.id)


# -------------------- UPDATE EVALUATION --------------------

@pytest.mark.asyncio
async def test_update_evaluation_by_evaluator(session, user, other_user, task_with_executor, evaluation):
    updated = await EvaluationService.update_evaluation(
        session, user, task_with_executor.id, other_user.id,
        data=EvaluationUpdateSchema(score=4, comment="Nice")
    )

    assert updated.score == 4
    assert updated.comment == "Nice"


@pytest.mark.asyncio
async def test_update_evaluation_forbidden(session, other_user, user, task_with_executor, evaluation):
    with pytest.raises(ForbiddenError):
        await EvaluationService.update_evaluation(
            session, other_user, task_with_executor.id, other_user.id,
            data=EvaluationUpdateSchema(score=1)
        )


# -------------------- DELETE EVALUATION --------------------

@pytest.mark.asyncio
async def test_delete_evaluation_by_evaluator(session, user, other_user, task_with_executor, evaluation):
    await EvaluationService.delete_evaluation(session, user, task_with_executor.id, other_user.id)

    with pytest.raises(NotFoundError):
        await EvaluationService.get_evaluation(session, user, task_with_executor.id, other_user.id)


@pytest.mark.asyncio
async def test_delete_evaluation_forbidden(session, other_user, user, task_with_executor, evaluation):
    with pytest.raises(ForbiddenError):
        await EvaluationService.delete_evaluation(session, other_user, task_with_executor.id, other_user.id)


# -------------------- GET AVERAGE --------------------

@pytest.mark.asyncio
async def test_get_average(session, user, other_user, task_with_executor, evaluation):
    task_2 = await TaskService.create_task(
        session,
        user,
        TaskCreateSchema(
            title="Task_0",
            description="Desc",
            deadline=None,
            executor_ids=[other_user.id]
        )
    )
    task_2.status = TaskStatus.done
    await session.commit()

    await EvaluationService.create_evaluation(
        session, user, task_2.id,
        EvaluationCreateSchema(score=4, comment="Good", executor_id=other_user.id)
    )

    avg = await EvaluationService.get_average(session, user, other_user.id, start=None, end=None)
    assert avg.user_id == other_user.id
    assert avg.count == 2
    assert avg.average_score == 4.5
