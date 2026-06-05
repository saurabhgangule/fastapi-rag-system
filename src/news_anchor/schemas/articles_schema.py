from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AddArticleSchema(BaseModel):
    title: str
    link: str
    image: Optional[str] = None
    summary: str
    topic_id: int
    published_at: Optional[datetime] = None


class ArticleSchema(BaseModel):
    id: int
    title: str
    link: str
    image: Optional[str] = None
    summary: str
    topic_id: int
    published_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
