from fastapi import APIRouter, status

from backend.api.core.decorators import handle_service_errors
from backend.api.core.dependencies import SessionDep, UserDep
from backend.schemas.meetings import MeetingPublicSchema, MeetingCreateSchema, MeetingListPublicSchema
from backend.services.meeting_service import MeetingService

router = APIRouter(prefix="/meetings", tags=["Встречи"])


@router.post("/",
             response_model=MeetingPublicSchema,
             status_code=status.HTTP_201_CREATED,
             summary="Создать встречу")
@handle_service_errors
async def create_meeting(data: MeetingCreateSchema, session: SessionDep, current_user: UserDep):
    return await MeetingService.create_meeting(session, current_user, data)


@router.get("/",
            response_model=list[MeetingListPublicSchema],
            summary="Получить мои встречи")
@handle_service_errors
async def get_my_meetings(session: SessionDep, current_user: UserDep):
    return await MeetingService.get_my_meetings(session, current_user)


@router.get(
    "/{meeting_id}",
    response_model=MeetingPublicSchema,
    summary="Получить встречу",
)
@handle_service_errors
async def get_meeting(meeting_id: int, session: SessionDep, current_user: UserDep):
    return await MeetingService.get_meeting(session, current_user, meeting_id)


@router.delete("/{meeting_id}",
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Удалить встречу")
@handle_service_errors
async def delete_meeting(meeting_id: int, session: SessionDep, current_user: UserDep):
    await MeetingService.delete_meeting(session, current_user, meeting_id)
