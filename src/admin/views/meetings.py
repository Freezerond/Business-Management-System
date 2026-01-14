from sqladmin import ModelView
from sqladmin.filters import ForeignKeyFilter

from src.models.meetings import Meeting
from src.models.teams import Team
from src.models.users import User


class MeetingAdmin(ModelView, model=Meeting):
    name = "Встреча"
    name_plural = "Встречи"
    icon = "fa-solid fa-calendar-days"

    column_list = [
        Meeting.id,
        Meeting.title,
        Meeting.description,
        Meeting.team,
        Meeting.creator,
        Meeting.start_time,
        Meeting.end_time,
        Meeting.participants,
    ]

    column_labels = {
        Meeting.title: "Название",
        Meeting.description: "Описание",
        Meeting.team: "Команда",
        Meeting.creator: "Создатель",
        Meeting.start_time: "Начало",
        Meeting.end_time: "Окончание",
        Meeting.participants: "Участники",
    }

    # Поиск
    column_searchable_list = [
        Meeting.title,
        Meeting.description,
    ]

    # Сортировка
    column_sortable_list = [
        Meeting.title,
        Meeting.start_time,
        Meeting.end_time,
    ]

    # Фильтрация
    column_filters = [
        ForeignKeyFilter(
            Meeting.team_id,
            foreign_display_field=Team.name,
            foreign_model=Team,
            title="Команда",
        ),
        ForeignKeyFilter(
            Meeting.creator_id,
            foreign_display_field=User.full_name,
            foreign_model=User,
            title="Создатель встречи",
        ),
    ]

    form_widget_args = {
        "start_time": {"format": "%Y-%m-%d %H:%M"},
        "end_time": {"format": "%Y-%m-%d %H:%M"},
    }
