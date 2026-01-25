import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.models.meetings import Meeting, MeetingParticipant
from backend.models.users import User, UserRole
from backend.schemas.meetings import MeetingCreateSchema
from backend.services.exceptions import ForbiddenError, ConflictError, NotFoundError
from backend.services.utils import safe_commit, get_object_or_404


class MeetingService:

    @staticmethod
    async def _check_time_conflicts(session: AsyncSession, user_ids: list[int], start_time: datetime.datetime, end_time: datetime.datetime) -> None:
        if not user_ids:
            return

        stmt = (
            select(MeetingParticipant.user_id)
            .join(Meeting)
            .where(
                MeetingParticipant.user_id.in_(user_ids),
                Meeting.start_time < end_time,
                Meeting.end_time > start_time
            )
        )
        conflicts = await session.scalars(stmt)
        conflicts = list(conflicts)
        if conflicts:
            raise ConflictError(f"У пользователя(ей) {conflicts} есть пересечение по времени")

    @staticmethod
    async def create_meeting(session: AsyncSession, creator: User, data: MeetingCreateSchema) -> Meeting:
        if creator.role not in (UserRole.admin, UserRole.manager):
            raise ForbiddenError("Вы не можете создавать встречи")

        if data.start_time >= data.end_time:
            raise ConflictError("Некорректное время встречи")
        if data.start_time.replace(tzinfo=None) < datetime.datetime.utcnow():
            raise ConflictError("Начало встречи не может быть в прошлом")

        participant_ids = set(data.participant_ids)
        participant_ids.add(creator.id)

        participants = (
            await session.scalars(
                select(User).where(
                    User.id.in_(participant_ids),
                    User.team_id == creator.team_id
                )
            )
        ).all()

        if len(participants) != len(participant_ids):
            raise ConflictError("Некоторые участники не принадлежат команде")

        start_time = data.start_time.astimezone(datetime.timezone.utc)
        end_time = data.end_time.astimezone(datetime.timezone.utc)

        await MeetingService._check_time_conflicts(session, list(participant_ids), start_time, end_time)

        meeting = Meeting(
            title=data.title,
            description=data.description,
            start_time=start_time,
            end_time=end_time,
            team_id=creator.team_id,
            creator_id=creator.id
        )
        meeting.participants = participants
        session.add(meeting)

        await safe_commit(session)
        await session.refresh(meeting, attribute_names=['participants'])
        meeting.participant_ids = [u.id for u in meeting.participants]
        return meeting

    @staticmethod
    async def get_meeting(session: AsyncSession, user: User, meeting_id: int) -> Meeting:
        stmt = (
            select(Meeting)
            .where(Meeting.id == meeting_id)
            .options(
                selectinload(Meeting.participants),
                selectinload(Meeting.creator)
            )
        )

        result = await session.execute(stmt)
        meeting = result.scalar_one_or_none()

        if not meeting:
            raise NotFoundError("Встреча не найдена")

        if meeting.team_id != user.team_id:
            raise ForbiddenError("Нет доступа к этой встрече")

        participant_ids = {u.id for u in meeting.participants}

        if (
                user.id != meeting.creator_id
                and user.id not in participant_ids
                and user.role != UserRole.admin
        ):
            raise ForbiddenError("Нет доступа к этой встрече")

        return meeting

    @staticmethod
    async def get_my_meetings(session: AsyncSession, user: User) -> list[Meeting]:
        await session.refresh(user, ['my_meetings'])
        return user.my_meetings

    @staticmethod
    async def delete_meeting(session: AsyncSession, user: User, meeting_id: int) -> None:
        meeting = await get_object_or_404(session, Meeting, meeting_id)

        if meeting.creator_id != user.id and user.role != UserRole.admin:
            raise ForbiddenError("Вы не можете отменить эту встречу")

        await session.delete(meeting)
        await safe_commit(session)

