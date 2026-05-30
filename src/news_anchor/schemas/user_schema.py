# These considered as the DTOs as well

from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

class CreateUserSchema(BaseModel):
    username: str
    email: EmailStr

class UserResponseSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)

class UserTopicsResponseSchema(BaseModel):
    user_id: int
    topic_id: int
    rss_link: str
    label: str

    model_config = ConfigDict(from_attributes=True)
