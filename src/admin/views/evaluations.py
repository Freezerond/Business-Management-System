from sqladmin import ModelView
from sqladmin.filters import ForeignKeyFilter

from src.models.evaluations import Evaluation
from src.models.tasks import Task
from src.models.users import User


class EvaluationAdmin(ModelView, model=Evaluation):
    name = "Оценка"
    name_plural = "Оценки"
    icon = "fa-solid fa-star"

    column_list = [
        Evaluation.task,
        Evaluation.executor,
        Evaluation.evaluator,
        Evaluation.score,
        Evaluation.comment,
        Evaluation.created_at,
    ]

    column_labels = {
        Evaluation.task: "Задача",
        Evaluation.executor: "Исполнитель",
        Evaluation.evaluator: "Оценил",
        Evaluation.score: "Оценка",
        Evaluation.comment: "Комментарий",
        Evaluation.created_at: "Дата",
    }

    # Поиск
    column_searchable_list = [
        Evaluation.comment,
    ]

    # Сортировка
    column_sortable_list = [
        Evaluation.created_at,
        Evaluation.score,
    ]

    # Фильтрация
    column_filters = [
        ForeignKeyFilter(
            Evaluation.task_id,
            foreign_display_field=Task.title,
            foreign_model=Task,
            title="Задача",
        ),
        ForeignKeyFilter(
            Evaluation.evaluator_id,
            foreign_display_field=User.full_name,
            foreign_model=User,
            title="Оценщик",
        ),
        ForeignKeyFilter(
            Evaluation.executor_id,
            foreign_display_field=User.full_name,
            foreign_model=User,
            title="Исполнитель",
        ),
    ]

    form_excluded_columns = [
        Evaluation.created_at,
        Evaluation.updated_at,
    ]
