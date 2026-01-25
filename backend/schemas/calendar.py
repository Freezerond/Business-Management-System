import datetime
import enum

from pydantic import BaseModel

from backend.models.tasks import TaskStatus


class CalendarEventType(str, enum.Enum):
    task = "task"
    meeting = "meeting"


class CalendarEventSchema(BaseModel):
    type: CalendarEventType
    id: int
    title: str

    date: datetime.date
    start_time: datetime.time | None = None
    end_time: datetime.time | None = None

    status: TaskStatus | None = None


class CalendarMonthSchema(BaseModel):
    date: datetime.date
    events: list[CalendarEventSchema]
