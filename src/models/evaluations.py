from sqlalchemy import ForeignKey, SmallInteger, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base, created_at, updated_at, str_1024


class Evaluation(Base):
    __tablename__ = 'evaluations'

    score: Mapped[int] = mapped_column(SmallInteger)
    comment: Mapped[str_1024]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    task_id: Mapped[int] = mapped_column(
        ForeignKey('tasks.id', ondelete='SET NULL'),
        primary_key=True
    )
    executor_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        primary_key=True
    )
    evaluator_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='SET NULL'))

    task: Mapped["Task"] = relationship(back_populates="evaluations")
    executor: Mapped["User"] = relationship(
        back_populates="evaluations_received",
        foreign_keys=[executor_id]
    )
    evaluator: Mapped["User"] = relationship(
        back_populates="evaluations_given",
        foreign_keys=[evaluator_id]
    )

    __table_args__ = (
        UniqueConstraint("task_id", "executor_id", "evaluator_id"),
        CheckConstraint("score >= 1 AND score <= 5"),
    )

    def __str__(self):
        return str(self.score)
