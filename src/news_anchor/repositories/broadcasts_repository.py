from datetime import datetime, timedelta

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
            broadcasted_at=broadcast_data.broadcasted_at,
        )
        self.db.add(broadcast)
        self.db.commit()
        self.db.refresh(broadcast)
        return broadcast

    def get_all_broadcasts(self):
        return self.db.query(Broadcast).all()

    def save_broadcast_mp3_url(self, broadcast_id: int, broadcast_mp3_url: str):
        broadcast = (
            self.db.query(Broadcast).filter(Broadcast.id == broadcast_id).first()
        )
        broadcast.broadcast_mp3_url = broadcast_mp3_url
        self.db.commit()
        self.db.refresh(broadcast)
        return broadcast

    def get_broadcasts_history(self, user_id: int):
        today_start = datetime.utcnow().replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        broadcasts_history = (
            self.db.query(Broadcast)
            .filter(
                Broadcast.user_id == user_id, Broadcast.broadcasted_at < today_start
            )
            .order_by(Broadcast.broadcasted_at.desc())
            .all()
        )

        return broadcasts_history if broadcasts_history else []

    def get_todays_broadcast(self, user_id: int):
        today_start = datetime.utcnow().replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        today_end = today_start + timedelta(days=1)

        todays_broadcast = (
            self.db.query(Broadcast)
            .filter(
                Broadcast.user_id == user_id,
                Broadcast.broadcasted_at >= today_start,
                Broadcast.broadcasted_at < today_end,
            )
            .order_by(Broadcast.broadcasted_at.desc())
            .first()
        )

        return todays_broadcast
