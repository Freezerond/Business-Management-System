from sqladmin import Admin

from src.admin.auth import AdminAuth
from src.admin.views.users import UserAdmin
from src.admin.views.teams import TeamAdmin
from src.admin.views.tasks import TaskAdmin, TaskCommentAdmin
from src.admin.views.evaluations import EvaluationAdmin
from src.admin.views.meetings import MeetingAdmin
from src.config import settings


def init_admin(app, engine):
    admin = Admin(
        app,
        engine,
        authentication_backend=AdminAuth(secret_key=settings.JWT_SECRET_KEY),
    )

    admin.add_view(UserAdmin)
    admin.add_view(TeamAdmin)
    admin.add_view(TaskAdmin)
    admin.add_view(TaskCommentAdmin)
    admin.add_view(EvaluationAdmin)
    admin.add_view(MeetingAdmin)

    return admin
