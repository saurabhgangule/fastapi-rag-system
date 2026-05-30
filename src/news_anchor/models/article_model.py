from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from .base import Base

class Article(Base): 
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    link = Column(String)
    image = Column(String)
    summary = Column(String)
    topic_id = Column(Integer, ForeignKey("topics.id"))
    published_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
