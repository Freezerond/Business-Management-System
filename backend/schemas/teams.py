import datetime
import uuid

from pydantic import BaseModel, constr, ConfigDict


class TeamCreateSchema(BaseModel):
    name: constr(max_length=64)


class TeamSchema(BaseModel):
    id: uuid.UUID
    name: str
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)
