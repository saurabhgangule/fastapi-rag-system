from sqlalchemy import Column, Integer, String
from .base import Base

class Topic(Base): 
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True)
    rss_link = Column(String)
    label = Column(String)