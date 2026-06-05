# These considered as the DTOs as well

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserResponseSchema(BaseModel):
    id: int
    name: str
    username: str
    email: EmailStr
    password: str
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class UserTopicsResponseSchema(BaseModel):
    user_id: int
    topic_id: int
    rss_link: str
    label: str

    model_config = ConfigDict(from_attributes=True)


class AddUserTopicSchema(BaseModel):
    topic_id: int
    success: bool
    message: str

    model_config = ConfigDict(from_attributes=True)
