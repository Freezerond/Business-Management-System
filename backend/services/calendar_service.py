import datetime
import calendar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.tasks import Task
from backend.models.meetings import Meeting, MeetingParticipant
from backend.models.users import User
from backend.schemas.calendar import CalendarEventSchema, CalendarMonthSchema


class CalendarService:

    @staticmethod
    async def get_day_events(session: AsyncSession, current_user: User, date: datetime.date):
        events: list[CalendarEventSchema] = []

        # Задачи на день
        tasks = (await session.scalars(
            select(Task)
            .where(
                Task.deadline == date,
                (Task.creator_id == current_user.id) | Task.executors.any(User.id == current_user.id)
            )
        )).all()

        for task in tasks:
            events.append(CalendarEventSchema(
                type="task",
                id=task.id,
                title=task.title,
                date=date,
                status=task.status
            ))

        # Встречи на день
        meetings = (await session.scalars(
            select(Meeting)
            .join(MeetingParticipant)
            .where(
                MeetingParticipant.user_id == current_user.id,
                Meeting.start_time.between(
                    datetime.datetime.combine(date, datetime.time.min),
                    datetime.datetime.combine(date, datetime.time.max)
                )
            )
        )).all()

        for meeting in meetings:
            events.append(CalendarEventSchema(
                type="meeting",
                id=meeting.id,
                title=meeting.title,
                date=date,
                start_time=meeting.start_time.time(),
                end_time=meeting.end_time.time()
            ))

        return sorted(events, key=lambda x: (x.start_time or datetime.time.min))

    @staticmethod
    async def get_month_events(session: AsyncSession, current_user: User, year: int, month: int):
        start = datetime.date(year, month, 1)
        end = datetime.date(year, month, calendar.monthrange(year, month)[1])

        result: dict[datetime.date, list[CalendarEventSchema]] = {}

        # Задачи за месяц
        tasks = (await session.scalars(
            select(Task)
            .where(
                Task.deadline.between(start, end),
                (Task.creator_id == current_user.id) | Task.executors.any(User.id == current_user.id)
            )
        )).all()

        for task in tasks:
            result.setdefault(task.deadline, []).append(
                CalendarEventSchema(
                    type="task",
                    id=task.id,
                    title=task.title,
                    date=task.deadline,
                    status=task.status
                )
            )

        # Встречи за месяц
        meetings = (await session.scalars(
            select(Meeting)
            .join(MeetingParticipant)
            .where(
                MeetingParticipant.user_id == current_user.id,
                Meeting.start_time.between(
                    datetime.datetime.combine(start, datetime.time.min),
                    datetime.datetime.combine(end, datetime.time.max)
                )
            )
        )).all()

        for meeting in meetings:
            day = meeting.start_time.date()
            result.setdefault(day, []).append(
                CalendarEventSchema(
                    type="meeting",
                    id=meeting.id,
                    title=meeting.title,
                    date=day,
                    start_time=meeting.start_time.time(),
                    end_time=meeting.end_time.time()
                )
            )

        return [CalendarMonthSchema(date=day, events=events) for day, events in sorted(result.items())]
