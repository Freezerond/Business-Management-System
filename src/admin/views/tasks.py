from sqladmin import ModelView
from sqladmin.filters import ForeignKeyFilter, StaticValuesFilter

from src.models.tasks import Task, TaskComment
from src.models.teams import Team
from src.models.users import User


class TaskAdmin(ModelView, model=Task):
    name = "Задача"
    name_plural = "Задачи"
    icon = "fa-solid fa-list-check"

    column_list = [
        Task.id,
        Task.title,
        Task.description,
        Task.status,
        Task.team,
        Task.creator,
        Task.deadline,
        Task.executors,
        Task.created_at,
    ]

    column_labels = {
        Task.title: "Название",
        Task.description: "Описание",
        Task.status: "Статус",
        Task.team: "Команда",
        Task.creator: "Создатель",
        Task.deadline: "Дедлайн",
        Task.executors: "Исполнители",
        Task.created_at: "Создана",
    }

    # Поиск
    column_searchable_list = [
        Task.title,
        Task.description,
    ]

    # Сортировка
    column_sortable_list = [
        Task.title,
        Task.deadline,
        Task.created_at,
    ]

    # Фильтрация
    column_filters = [
        StaticValuesFilter(
            Task.status,
            values=[("open", "Open"), ("in_progress", "In progress "), ("done", "Done")],
        ),
        ForeignKeyFilter(
            Task.team_id,
            foreign_display_field=Team.name,
            foreign_model=Team,
            title="Команда",
        ),
        ForeignKeyFilter(
            Task.creator_id,
            foreign_display_field=User.full_name,
            foreign_model=User,
            title="Создатель задачи",
        ),
    ]

    form_excluded_columns = [
        Task.comments,
        Task.evaluations,
        Task.created_at,
        Task.updated_at,
    ]

    form_widget_args = {
        "created_at": {"readonly": True},
        "updated_at": {"readonly": True},
    }


class TaskCommentAdmin(ModelView, model=TaskComment):
    name = "Комментарий"
    name_plural = "Комментарии"
    icon = "fa-solid fa-comments"

    column_list = [
        TaskComment.id,
        TaskComment.task,
        TaskComment.author,
        TaskComment.message,
        TaskComment.created_at,
    ]

    column_labels = {
        TaskComment.task: "Задача",
        TaskComment.author: "Автор",
        TaskComment.message: "Сообщение",
        TaskComment.created_at: "Дата",
    }

    # Поиск
    column_searchable_list = [
        TaskComment.message,
    ]

    # Сортировка
    column_sortable_list = [
        TaskComment.created_at,
    ]

    # Фильтрация
    column_filters = [
        ForeignKeyFilter(
            TaskComment.task_id,
            foreign_display_field=Task.title,
            foreign_model=Task,
            title="Задача",
        ),
        ForeignKeyFilter(
            TaskComment.author_id,
            foreign_display_field=User.full_name,
            foreign_model=User,
            title="Автор комментария",
        ),
    ]

    form_excluded_columns = [
        TaskComment.created_at,
    ]
