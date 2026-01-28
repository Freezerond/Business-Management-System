"""
Скрипт для создания суперадминистратора.
Запускается вручную из терминала.
Пример запуска:
    python -m create_admin
"""


import asyncio

from getpass import getpass

from backend.database import async_session
from backend.models.users import User, UserRole
from backend.models import teams, tasks, evaluations, meetings
from backend.services.user_service import UserService
from backend.services.utils import safe_commit
from backend.services.security import hash_password


async def create_superadmin():
    email = input("Введите email: ").strip()
    full_name = input("Введите полное имя: ").strip()
    password = getpass("Введите пароль: ").strip()

    async with async_session() as session:
        existing = await UserService.get_by_email(session, email)
        if existing:
            print(f"Пользователь с email {email} уже существует!")
            return

        user = User(
            email=email,
            full_name=full_name,
            password=hash_password(password),
            role=UserRole.admin
        )
        session.add(user)

        try:
            await safe_commit(session)
            print(f"admin {full_name} успешно создан!")
        except Exception as e:
            print(f"Ошибка при создании superadmin: {e}")


if __name__ == "__main__":
    asyncio.run(create_superadmin())
