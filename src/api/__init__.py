from fastapi import APIRouter

from src.api.routers.auth import auth_router
from src.api.routers.users import users_router
from src.api.routers.teams import router as teams_router
from src.api.routers.tasks import router as tasks_router
from src.api.routers.evaluations import router as evaluations_router
from src.api.routers.meetings import router as meetings_router
from src.api.routers.calendar import router as calendar_router

main_router = APIRouter()
main_router.include_router(auth_router)
main_router.include_router(users_router)
main_router.include_router(teams_router)
main_router.include_router(tasks_router)
main_router.include_router(evaluations_router)
main_router.include_router(meetings_router)
main_router.include_router(calendar_router)
