import datetime
import uuid

from pydantic import BaseModel, constr, EmailStr, Field, ConfigDict

from src.models.users import UserRole


class UserBaseSchema(BaseModel):
    id: int | None = Field(None, readOnly=True)
    email: EmailStr = Field(..., max_length=64)
    full_name: constr(max_length=255)


class UserCreateSchema(UserBaseSchema):
    password: constr(min_length=8)


class UserUpdateSchema(BaseModel):
    email: EmailStr | None = Field(None, max_length=64)
    full_name: constr(max_length=255) | None = None
    password: constr(min_length=8) | None = None


class UserPublicSchema(UserBaseSchema):
    role: UserRole
    created_at: datetime.datetime
    team_id: uuid.UUID | None = None

    model_config = ConfigDict(from_attributes=True)
