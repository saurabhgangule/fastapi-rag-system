from sqlalchemy.orm import Session
from news_anchor.repositories.broadcasts_repository import BroadcastsRepository
from news_anchor.schemas.broadcasts_schema import AddBroadcastSchema

class BroadcastsService:

    def __init__(self, db: Session) -> None:
        self.broadcasts_repository = BroadcastsRepository(db)

    def add_broadcast(self, broadcast_data: AddBroadcastSchema):
        return self.broadcasts_repository.add_broadcast(broadcast_data)

    def get_all_broadcasts(self):
        return self.broadcasts_repository.get_all_broadcasts()

    def save_broadcast_mp3_url(self, broadcast_id: int, broadcast_mp3_url: str):
        save_result = self.broadcasts_repository.save_broadcast_mp3_url(broadcast_id, broadcast_mp3_url)
        
        if save_result:
            return True
        else:
            return False