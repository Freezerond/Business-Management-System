import uuid

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.services.exceptions import ConflictError, NotFoundError


async def get_object_or_404(session: AsyncSession, model, obj_id: int | uuid.UUID):
    obj = await session.get(model, obj_id)
    if not obj:
        raise NotFoundError(f"{model.__name__} с id={obj_id} не найден(а)")
    return obj


async def safe_commit(session):
    """
    Производит commit и rollback при ошибках.
    """
    try:
        await session.commit()
    except IntegrityError as ex:
        await session.rollback()
        raise ConflictError("Ошибка при обновлении данных") from ex
