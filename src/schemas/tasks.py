import uuid

from pydantic import BaseModel, constr, ConfigDict, Field
from datetime import date, datetime

from src.models.tasks import TaskStatus
from src.schemas.users import UserPublicSchema


class TaskBaseSchema(BaseModel):
    title: constr(max_length=256)
    description: constr(max_length=1024) | None = None
    deadline: date | None = None


class TaskCreateSchema(TaskBaseSchema):
    executor_ids: list[int] = []


class TaskUpdateSchema(BaseModel):
    title: constr(max_length=256) | None = None
    description: constr(max_length=1024) | None = None
    deadline: date | None = None
    executor_ids: list[int] | None = None


class TaskListPublicSchema(TaskBaseSchema):
    id: int
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    creator_id: int
    team_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)


class TaskPublicSchema(TaskListPublicSchema):
    executors: list[UserPublicSchema] = Field(default_factory=list)


class TaskStatusUpdateSchema(BaseModel):
    status: TaskStatus


class TaskCommentCreateSchema(BaseModel):
    message: constr(max_length=1024)


class TaskCommentPublicSchema(TaskCommentCreateSchema):
    id: int
    task_id: int
    author_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
