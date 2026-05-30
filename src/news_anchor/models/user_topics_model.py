from sqlalchemy import Column, ForeignKey, Integer, DateTime
from datetime import datetime
from .base import Base

class UserTopics(Base): 
    __tablename__ = "user_topics"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    topic_id = Column(Integer, ForeignKey("topics.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
