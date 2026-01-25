from sqladmin.authentication import AuthenticationBackend
from fastapi.requests import Request

from backend.models.users import UserRole
from backend.services.security import verify_password
from backend.services.user_service import UserService
from backend.database import async_session


class AdminAuth(AuthenticationBackend):

    async def login(self, request: Request) -> bool:
        form = await request.form()
        email = form.get("username")
        password = form.get("password")

        async with async_session() as session:
            user = await UserService.get_by_email(session, email)

            if not user:
                return False
            if not verify_password(password, user.password):
                return False
            if user.role != UserRole.superadmin:
                return False

        request.session["user_id"] = str(user.id)
        request.session["user_role"] = user.role.value

        return True

    async def authenticate(self, request: Request) -> bool:
        user_id = request.session.get("user_id")
        role = request.session.get("user_role")

        if not user_id or role != UserRole.superadmin.value:
            return False

        async with async_session() as session:
            user = await UserService.get_by_id(session, int(user_id))

        request.state.user = user
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True
