from sqladmin import Admin

from backend.admin.auth import AdminAuth
from backend.admin.views.users import UserAdmin
from backend.admin.views.teams import TeamAdmin
from backend.admin.views.tasks import TaskAdmin, TaskCommentAdmin
from backend.admin.views.evaluations import EvaluationAdmin
from backend.admin.views.meetings import MeetingAdmin
from backend.config import settings


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
