from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from .base import Base

class Broadcast(Base): 
    __tablename__ = "broadcasts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    broadcast_summary = Column(String)
    broadcast_mp3_url = Column(String)
    broadcasted_at = Column(DateTime)
