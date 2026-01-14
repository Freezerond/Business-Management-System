from fastapi import FastAPI

from src.api import main_router
from src.admin.admin_app import init_admin
from src.database import async_engine

app = FastAPI(
    title="Business Management System",
    description="Веб-приложение для управления командой внутри компании"
)

init_admin(app, async_engine)
app.include_router(main_router)
