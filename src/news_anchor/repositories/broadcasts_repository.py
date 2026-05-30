from sqlalchemy.orm import Session
from news_anchor.models.broadcast_model import Broadcast
from news_anchor.schemas.broadcasts_schema import AddBroadcastSchema

class BroadcastsRepository:

    def __init__(self, db: Session) -> None:
        self.db = db

    def add_broadcast(self, broadcast_data: AddBroadcastSchema):
        broadcast = Broadcast(
            user_id=broadcast_data.user_id,
            broadcast_summary=broadcast_data.broadcast_summary,
            broadcast_mp3_url=broadcast_data.broadcast_mp3_url,
            broadcasted_at=broadcast_data.broadcasted_at
        )
        self.db.add(broadcast)
        self.db.commit()
        self.db.refresh(broadcast)
        return broadcast

    def get_all_broadcasts(self):
        return self.db.query(Broadcast).all()

    def save_broadcast_mp3_url(self, broadcast_id: int, broadcast_mp3_url: str):
        broadcast = self.db.query(Broadcast).filter(Broadcast.id == broadcast_id).first()
        broadcast.broadcast_mp3_url = broadcast_mp3_url
        self.db.commit()
        self.db.refresh(broadcast)
        return broadcast