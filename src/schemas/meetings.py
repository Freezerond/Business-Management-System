import datetime

from pydantic import BaseModel, constr, ConfigDict, Field

from src.schemas.users import UserPublicSchema


class MeetingCreateSchema(BaseModel):
    title: constr(max_length=256)
    description: constr(max_length=1024) | None = None
    start_time: datetime.datetime
    end_time: datetime.datetime
    participant_ids: list[int] = []


class MeetingListPublicSchema(BaseModel):
    id: int
    title: str
    description: str | None
    start_time: datetime.datetime
    end_time: datetime.datetime
    creator_id: int

    model_config = ConfigDict(from_attributes=True)


class MeetingPublicSchema(MeetingListPublicSchema):
    participants: list[UserPublicSchema] = Field(default_factory=list)
