from pydantic import BaseModel


class AddTopicSchema(BaseModel):
    rss_link: str
    label: str


class TopicResponseSchema(BaseModel):
    id: int
    rss_link: str
    label: str
