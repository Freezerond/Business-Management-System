from pydantic import BaseModel, EmailStr, constr


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class LoginInput(BaseModel):
    email: EmailStr
    password: constr(min_length=8)
