import pytest

from src.services.task_service import TaskService
from src.services.exceptions import ForbiddenError, ConflictError, NotFoundError
from src.models.tasks import TaskComment
from src.services.utils import get_object_or_404


@pytest.mark.asyncio
async def test_create_comment_by_creator(session, user, task):
    comment = await TaskService.create_comment(
        session,
        user,
        task.id,
        "Comment"
    )

    assert isinstance(comment, TaskComment)
    assert comment.message == "Comment"


@pytest.mark.asyncio
async def test_create_comment_by_executor(session, other_user, task_with_executor):
    comment = await TaskService.create_comment(
        session,
        other_user,
        task_with_executor.id,
        "Comment"
    )

    assert comment.author_id == other_user.id


@pytest.mark.asyncio
async def test_create_comment_by_outsider_forbidden(session, other_user, task):
    with pytest.raises(ForbiddenError):
        await TaskService.create_comment(
            session,
            other_user,
            task.id,
            "Hack"
        )


@pytest.mark.asyncio
async def test_get_comments(session, user, other_user, task_with_executor):
    await TaskService.create_comment(session, user, task_with_executor.id, "One")
    await TaskService.create_comment(session, other_user, task_with_executor.id, "Two")

    comments = await TaskService.get_comments(session, user, task_with_executor.id)
    assert len(comments) == 2


@pytest.mark.asyncio
async def test_delete_own_comment(session, user, task):
    comment = await TaskService.create_comment(session, user, task.id, "Comment")

    await TaskService.delete_comment(session, user, task.id, comment.id)

    with pytest.raises(NotFoundError):
        await get_object_or_404(session, TaskComment, comment.id)


@pytest.mark.asyncio
async def test_delete_comment_by_other_user_forbidden(session, user, other_user, task_with_executor):
    comment = await TaskService.create_comment(session, user, task_with_executor.id, "Comment")

    with pytest.raises(ForbiddenError):
        await TaskService.delete_comment(session, other_user, task_with_executor.id, comment.id)


@pytest.mark.asyncio
async def test_delete_comment_wrong_task_conflict(session, user, task):
    comment = await TaskService.create_comment(session, user, task.id, "Comment")

    with pytest.raises(ConflictError):
        await TaskService.delete_comment(session, user, task.id + 1, comment.id)
