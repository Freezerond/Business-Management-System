from typing import Annotated
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.database import get_session
from src.models.users import User
from src.services.exceptions import NotFoundError, UnauthorizedError
from src.services.jwt_manager import verify_token
from src.services.user_service import UserService

SessionDep = Annotated[AsyncSession, Depends(get_session)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        session: SessionDep = None
) -> User:
    """
    Зависимость для получения текущего авторизованного пользователя
    """
    try:
        payload = verify_token(token)
        user_id = payload.get("sub")
        user = await UserService.get_by_id(session, int(user_id))
        return user
    except (JWTError, NotFoundError, UnauthorizedError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не авторизован")


UserDep = Annotated[User, Depends(get_current_user)]
