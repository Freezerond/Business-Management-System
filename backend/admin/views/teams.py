from sqladmin import ModelView

from backend.models.teams import Team


class TeamAdmin(ModelView, model=Team):
    name = "Команда"
    name_plural = "Команды"
    icon = "fa-solid fa-building"

    column_list = [
        Team.id,
        Team.name,
        Team.created_at,
        Team.users,
    ]

    column_labels = {
        Team.name: "Название",
        Team.created_at: "Создана",
        Team.users: "Участники",
    }

    # Поиск
    column_searchable_list = [
        Team.name,
    ]

    # Сортировка
    column_sortable_list = [
        Team.name,
        Team.created_at,
    ]

    form_excluded_columns = [
        Team.tasks,
        Team.meetings,
        Team.created_at,
        Team.users,
    ]

    form_widget_args = {
        "created_at": {"readonly": True},
    }
