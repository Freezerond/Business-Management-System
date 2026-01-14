import enum
import uuid

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base, str_64, str_256, intpk, created_at, updated_at


class UserRole(str, enum.Enum):
    user = "user"
    employee = "employee"
    manager = "manager"
    admin = "admin"
    superadmin = "superadmin"


class User(Base):
    __tablename__ = 'users'

    id: Mapped[intpk]
    email: Mapped[str_64] = mapped_column(unique=True)
    full_name: Mapped[str_256]
    password: Mapped[str_256]
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, native_enum=True), default=UserRole.user
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    team_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey('teams.id', ondelete='SET NULL'))

    team: Mapped["Team"] = relationship(back_populates="users")
    created_tasks: Mapped[list["Task"]] = relationship(
        back_populates="creator",
        foreign_keys="Task.creator_id",
    )
    my_tasks: Mapped[list["Task"]] = relationship(
        back_populates="executors",
        secondary="task_executors"
    )
    task_comments: Mapped[list["TaskComment"]] = relationship(
        back_populates="author",
        foreign_keys="TaskComment.author_id"
    )
    evaluations_given: Mapped[list["Evaluation"]] = relationship(
        back_populates="evaluator",
        foreign_keys="Evaluation.evaluator_id",
    )
    evaluations_received: Mapped[list["Evaluation"]] = relationship(
        back_populates="executor",
        foreign_keys="Evaluation.executor_id",
    )
    created_meetings: Mapped[list["Meeting"]] = relationship(
        back_populates="creator",
        foreign_keys="Meeting.creator_id"
    )
    my_meetings: Mapped[list["Meeting"]] = relationship(
        back_populates="participants",
        secondary="meeting_participants"
    )

    def __str__(self):
        if self.full_name:
            return self.full_name
        return self.email
