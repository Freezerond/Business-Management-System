import datetime

from pydantic import BaseModel, conint, constr, ConfigDict


class EvaluationBaseSchema(BaseModel):
    score: conint(ge=1, le=5)
    comment: constr(max_length=1024)


class EvaluationCreateSchema(EvaluationBaseSchema):
    executor_id: int


class EvaluationUpdateSchema(BaseModel):
    score: conint(ge=1, le=5) | None = None
    comment: constr(max_length=1024) | None = None


class EvaluationPublicSchema(EvaluationBaseSchema):
    task_id: int
    executor_id: int
    evaluator_id: int
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class AvgEvaluationSchema(BaseModel):
    user_id: int
    average_score: float
    count: int
    start_date: datetime.date | None = None
    end_date: datetime.date | None = None
