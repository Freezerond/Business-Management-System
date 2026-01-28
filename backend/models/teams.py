import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, relationship, mapped_column

from backend.database import Base, str_64, created_at


class Team(Base):
    __tablename__ = 'teams'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str_64]
    created_at: Mapped[created_at]

    users: Mapped[list["User"]] = relationship(back_populates="team")
    tasks: Mapped[list["Task"]] = relationship(back_populates="team", cascade="all, delete-orphan")
    meetings: Mapped[list["Meeting"]] = relationship(back_populates="team", cascade="all, delete-orphan")

    def __str__(self):
        return self.name
