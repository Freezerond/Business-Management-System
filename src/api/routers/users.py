from fastapi import APIRouter, HTTPException, status

from src.schemas.users import UserPublicSchema, UserUpdateSchema
from src.services.user_service import UserService
from src.services.exceptions import ConflictError
from src.api.core.dependencies import SessionDep, UserDep

users_router = APIRouter(prefix="/users", tags=["Пользователи"])


@users_router.get("/my_profile",
                  response_model=UserPublicSchema,
                  summary="Получить профиль пользователя")
async def get_my_profile(current_user: UserDep):
    return current_user


@users_router.patch("/my_profile",
                    response_model=UserPublicSchema,
                    summary="Изменить информацию о пользователе")
async def update_my_profile(data: UserUpdateSchema, session: SessionDep, current_user: UserDep):
    try:
        updated_user = await UserService.update_profile(session, current_user, data)
        return updated_user
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@users_router.delete("/my_profile",
                     status_code=status.HTTP_204_NO_CONTENT,
                     summary="Удалить пользователя")
async def delete_my_profile(session: SessionDep, current_user: UserDep):
    await UserService.delete_user(session, current_user)
