from typing import Any

from sqladmin import ModelView
from sqladmin.filters import StaticValuesFilter, ForeignKeyFilter
from starlette.requests import Request

from src.models.teams import Team
from src.models.users import User
from src.services.security import hash_password


class UserAdmin(ModelView, model=User):
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"

    column_list = [
        User.id,
        User.email,
        User.full_name,
        User.role,
        User.team,
        User.created_at,
    ]

    column_labels = {
        User.full_name: "ФИО",
        User.created_at: "Создан",
        User.team: "Команда",
    }

    # Поиск
    column_searchable_list = [
        User.email,
        User.full_name,
    ]

    # Сортировка
    column_sortable_list = [
        User.full_name,
        User.created_at,
        User.email,
    ]

    # Фильтрация
    column_filters = [
        StaticValuesFilter(
            User.role,
            values=[("admin", "Admin"), ("user", "User"), ("manager", "Manager")],
        ),
        ForeignKeyFilter(
            User.team_id,
            foreign_display_field=Team.name,
            foreign_model=Team,
            title="Команда",
        ),
    ]

    form_excluded_columns = [
        User.created_at,
        User.updated_at,
        User.created_tasks,
        User.my_tasks,
        User.task_comments,
        User.evaluations_given,
        User.evaluations_received,
        User.created_meetings,
        User.my_meetings,
    ]

    form_widget_args = {
        "created_at": {"readonly": True},
        "updated_at": {"readonly": True},
    }

    async def on_model_change(self, data: dict, model: Any, is_created: bool, request: Request) -> None:
        password = data.get("password")
        if password:
            data["password"] = hash_password(password)
