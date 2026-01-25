from sqlalchemy.ext.asyncio import AsyncSession

from backend.services.user_service import UserService
from backend.services.security import verify_password
from backend.services.jwt_manager import create_access_token, create_refresh_token, verify_token
from backend.services.exceptions import UnauthorizedError
from backend.schemas.auth import LoginInput


class AuthService:

    @staticmethod
    async def login(session: AsyncSession, data: LoginInput) -> dict:
        user = await UserService.get_by_email(session, data.email)
        if not user or not verify_password(data.password, user.password):
            raise UnauthorizedError("Неверный email или пароль")
        access_token = create_access_token({"sub": str(user.id), "role": user.role.value})
        refresh_token = create_refresh_token({"sub": str(user.id)})
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

    @staticmethod
    async def refresh(session: AsyncSession, refresh_token: str) -> dict:
        """
        Использует refresh-токен для повторной аутентификации пользователя.
        Выполняет обновление access-токена.
        """
        payload = verify_token(refresh_token)
        if not payload:
            raise UnauthorizedError("Неверный refresh token")
        user_id = payload.get("sub")
        user = await UserService.get_by_id(session, int(user_id))
        access_token = create_access_token({"sub": str(user.id), "role": user.role.value})
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
