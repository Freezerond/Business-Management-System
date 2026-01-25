import datetime
import uuid

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base, str_256, str_1024, intpk


class Meeting(Base):
    __tablename__ = 'meetings'

    id: Mapped[intpk]
    title: Mapped[str_256]
    description: Mapped[str_1024]
    start_time: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_time: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    team_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('teams.id', ondelete="CASCADE"))
    creator_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="SET NULL"))

    team: Mapped["Team"] = relationship(back_populates="meetings")
    creator: Mapped["User"] = relationship(back_populates="created_meetings")
    participants: Mapped[list["User"]] = relationship(
        back_populates="my_meetings",
        secondary="meeting_participants",
    )

    def __str__(self):
        return self.title


class MeetingParticipant(Base):
    __tablename__ = 'meeting_participants'

    meeting_id: Mapped[int] = mapped_column(
        ForeignKey('meetings.id', ondelete="CASCADE"),
        primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete="CASCADE"),
        primary_key=True
    )
