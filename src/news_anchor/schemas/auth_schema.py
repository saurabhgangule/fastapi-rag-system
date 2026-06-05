# These considered as the DTOs as well

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(from_attributes=True)


class RegisterUserSchema(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str

    model_config = ConfigDict(from_attributes=True)


class AuthResponseSchema(BaseModel):
    access_token: str
    token_type: str = "Bearer"
