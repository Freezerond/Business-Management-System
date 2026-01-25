import enum
import datetime
import uuid

from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base, str_256, str_1024, intpk, created_at, updated_at


class TaskStatus(enum.Enum):
    open = "open"
    in_progress = "in_progress"
    done = "done"


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[intpk]
    title: Mapped[str_256]
    description: Mapped[str_1024]
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus, native_enum=True), default=TaskStatus.open
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    deadline: Mapped[datetime.date | None]
    team_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=False)

    team: Mapped["Team"] = relationship(back_populates="tasks")
    creator: Mapped["User"] = relationship(back_populates="created_tasks")
    executors: Mapped[list["User"]] = relationship(
        back_populates="my_tasks",
        secondary="task_executors"
    )
    evaluations: Mapped[list["Evaluation"]] = relationship(back_populates="task")
    comments: Mapped[list["TaskComment"]] = relationship(back_populates="task")

    def __str__(self):
        return self.title


class TaskExecutor(Base):
    __tablename__ = 'task_executors'

    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"),
        primary_key=True
    )
    executor_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    )


class TaskComment(Base):
    __tablename__ = 'task_comments'

    id: Mapped[intpk]
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"))
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))

    created_at: Mapped[created_at]
    message: Mapped[str_1024]

    task: Mapped["Task"] = relationship(back_populates="comments")
    author: Mapped["User"] = relationship(back_populates="task_comments")

    def __str__(self):
        return self.message
