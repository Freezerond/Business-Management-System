from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.users import User
from src.schemas.users import UserCreateSchema, UserUpdateSchema
from src.services.utils import safe_commit, get_object_or_404
from src.services.security import hash_password
from src.services.exceptions import ConflictError


class UserService:

    @staticmethod
    async def get_by_id(session: AsyncSession, user_id: int) -> User:
        """Находит и возвращает пользователя по id."""
        return await get_object_or_404(session, User, user_id)

    @staticmethod
    async def get_by_email(session: AsyncSession, email: str) -> User | None:
        """Находит и возвращает пользователя по email."""
        return await session.scalar(select(User).where(User.email == email))

    @staticmethod
    async def create_user(session: AsyncSession, data: UserCreateSchema) -> User:
        existing = await UserService.get_by_email(session, data.email)

        if existing:
            raise ConflictError(f"Пользователь с email {data.email} уже зарегистрирован")

        user = User(
            email=data.email,
            full_name=data.full_name,
            password=hash_password(data.password),
        )
        session.add(user)
        await safe_commit(session)
        await session.refresh(user)
        return user

    @staticmethod
    async def update_profile(session: AsyncSession, user: User, data: UserUpdateSchema) -> User:
        update_data = data.model_dump(exclude_unset=True)

        if "email" in update_data:
            existing = await UserService.get_by_email(session, update_data["email"])
            if existing and existing.id != user.id:
                raise ConflictError(f"Пользователь с email {update_data['email']} уже существует")

        if "password" in update_data:
            update_data["password"] = hash_password(update_data["password"])

        for field, value in update_data.items():
            setattr(user, field, value)
        await safe_commit(session)
        await session.refresh(user)
        return user

    @staticmethod
    async def delete_user(session: AsyncSession, user: User) -> None:
        await session.delete(user)
        await safe_commit(session)
