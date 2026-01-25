from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api import main_router
from backend.admin.admin_app import init_admin
from backend.database import async_engine

app = FastAPI(
    title="Business Management System",
    description="Веб-приложение для управления командой внутри компании"
)

init_admin(app, async_engine)
app.include_router(main_router)


origins = [
    "http://localhost:300",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
