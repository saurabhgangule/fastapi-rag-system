from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AddBroadcastSchema(BaseModel):
    user_id: int
    broadcast_summary: str
    broadcast_mp3_url: Optional[str] = None
    broadcasted_at: Optional[datetime] = None


class BroadcastResponseSchema(BaseModel):
    id: int
    broadcast_summary: str
    broadcast_mp3_url: Optional[str] = None
    broadcasted_at: Optional[datetime] = None
