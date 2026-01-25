from fastapi import APIRouter, HTTPException, status, Form
from jose import JWTError
from pydantic import ValidationError

from backend.schemas.users import UserCreateSchema, UserPublicSchema
from backend.schemas.auth import LoginInput, Token
from backend.services.user_service import UserService
from backend.services.auth_service import AuthService
from backend.services.exceptions import ConflictError, UnauthorizedError, NotFoundError
from backend.api.core.dependencies import SessionDep

auth_router = APIRouter(prefix="/auth", tags=["Авторизация"])


@auth_router.post("/register",
                  response_model=UserPublicSchema,
                  status_code=status.HTTP_201_CREATED,
                  summary="Зарегестрировать пользователя")
async def register(user_data: UserCreateSchema, session: SessionDep):
    try:
        user = await UserService.create_user(session, user_data)
        return user

    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@auth_router.post("/login",
                  response_model=Token,
                  summary="Войти в аккаунт пользователя")
async def login(session: SessionDep, username: str = Form(...), password: str = Form(...)):
    try:
        data = LoginInput(email=username, password=password)
        token_data = await AuthService.login(session, data)
        return token_data

    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Некорректный email или пароль"
        )

    except UnauthorizedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@auth_router.post("/refresh",
                  response_model=Token,
                  summary="Обновить refresh токен")
async def refresh_token(refresh_token: str, session: SessionDep):
    try:
        token_data = await AuthService.refresh(session, refresh_token)
        return token_data
    except (JWTError, UnauthorizedError, NotFoundError) as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
