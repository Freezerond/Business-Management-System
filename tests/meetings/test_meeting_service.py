import pytest
import datetime
from src.models.meetings import Meeting
from src.schemas.meetings import MeetingCreateSchema
from src.services.meeting_service import MeetingService
from src.services.exceptions import ConflictError, ForbiddenError, NotFoundError


# -------------------- CREATE MEETING --------------------

@pytest.mark.asyncio
async def test_create_meeting_by_admin(session, user, other_user, team_with_member, time_slot):
    start, end = time_slot

    meeting = await MeetingService.create_meeting(
        session,
        user,
        MeetingCreateSchema(
            title="Planning",
            description="Project planning",
            start_time=start,
            end_time=end,
            participant_ids=[other_user.id]
        )
    )

    assert isinstance(meeting, Meeting)
    assert meeting.creator_id == user.id
    assert user in meeting.participants
    assert other_user in meeting.participants
    assert meeting.start_time == start
    assert meeting.end_time == end


@pytest.mark.asyncio
async def test_create_meeting_by_employee_forbidden(session, other_user, team_with_member, time_slot):
    start, end = time_slot

    with pytest.raises(ForbiddenError):
        await MeetingService.create_meeting(
            session,
            other_user,
            MeetingCreateSchema(
                title="Hack",
                description="Try create",
                start_time=start,
                end_time=end,
                participant_ids=[]
            )
        )


@pytest.mark.asyncio
async def test_create_meeting_with_invalid_time(session, user, team):
    start = datetime.datetime.utcnow() + datetime.timedelta(days=1)
    end = start - datetime.timedelta(hours=1)

    with pytest.raises(ConflictError):
        await MeetingService.create_meeting(
            session,
            user,
            MeetingCreateSchema(
                title="Invalid Time",
                description="Wrong",
                start_time=start,
                end_time=end,
                participant_ids=[]
            )
        )


@pytest.mark.asyncio
async def test_create_meeting_with_participant_outside_team(session, user, team, other_user, time_slot):
    start, end = time_slot

    with pytest.raises(ConflictError):
        await MeetingService.create_meeting(
            session,
            user,
            MeetingCreateSchema(
                title="Outsider",
                description="Not in team",
                start_time=start,
                end_time=end,
                participant_ids=[other_user.id] if other_user else []
            )
        )


@pytest.mark.asyncio
async def test_create_meeting_with_time_conflict(session, user, other_user, meeting_with_participant):
    start = meeting_with_participant.start_time + datetime.timedelta(minutes=30)
    end = start + datetime.timedelta(hours=1)

    with pytest.raises(ConflictError):
        await MeetingService.create_meeting(
            session,
            user,
            MeetingCreateSchema(
                title="Conflict",
                description="Overlap",
                start_time=start,
                end_time=end,
                participant_ids=[other_user.id]
            )
        )


# -------------------- GET MY MEETINGS --------------------

@pytest.mark.asyncio
async def test_get_my_meetings(session, user, meeting_with_participant):
    meetings = await MeetingService.get_my_meetings(session, user)
    assert meeting_with_participant in meetings


# -------------------- DELETE MEETING --------------------

@pytest.mark.asyncio
async def test_delete_meeting_by_creator(session, user, meeting_with_participant):
    await MeetingService.delete_meeting(session, user, meeting_with_participant.id)

    with pytest.raises(NotFoundError):
        await MeetingService.get_meeting(session, user, meeting_with_participant.id)


@pytest.mark.asyncio
async def test_delete_meeting_by_non_creator_forbidden(session, other_user, meeting_with_participant):
    with pytest.raises(ForbiddenError):
        await MeetingService.delete_meeting(session, other_user, meeting_with_participant.id)
