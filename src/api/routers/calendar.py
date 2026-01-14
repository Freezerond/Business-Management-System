import datetime

from fastapi import APIRouter

from src.schemas.calendar import CalendarEventSchema, CalendarMonthSchema
from src.services.calendar_service import CalendarService
from src.api.core.dependencies import SessionDep, UserDep
from src.api.core.decorators import handle_service_errors

router = APIRouter(prefix="/calendar", tags=["Календарь"])


@router.get('/day',
            response_model=list[CalendarEventSchema],
            summary="Получить дневной календарь")
@handle_service_errors
async def calendar_day(date: datetime.date, session: SessionDep, current_user: UserDep):
    return await CalendarService.get_day_events(session, current_user, date)


@router.get('/month',
            response_model=list[CalendarMonthSchema],
            summary="Получить месячный календарь")
@handle_service_errors
async def calendar_month(year: int, month: int, session: SessionDep, current_user: UserDep):
    return await CalendarService.get_month_events(session, current_user, year, month)
