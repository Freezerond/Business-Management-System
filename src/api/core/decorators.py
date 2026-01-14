from functools import wraps
from fastapi import HTTPException, status

from src.services.exceptions import ForbiddenError, NotFoundError, ConflictError


def handle_service_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ForbiddenError as ex:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(ex))
        except NotFoundError as ex:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ex))
        except ConflictError as ex:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))
    return wrapper
