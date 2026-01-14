from fastapi import APIRouter, HTTPException, status, Form
from jose import JWTError

from src.schemas.users import UserCreateSchema, UserPublicSchema
from src.schemas.auth import LoginInput, Token
from src.services.user_service import UserService
from src.services.auth_service import AuthService
from src.services.exceptions import ConflictError, UnauthorizedError, NotFoundError
from src.api.core.dependencies import SessionDep

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
