from sqlalchemy.orm import Session
from news_anchor.models.topic_model import Topic

class TopicsRepository:

    def __init__(self, db: Session) -> None:
        self.db = db

    def create_topic(self, rss_link: str, label: str):
        topic = Topic(
            rss_link=rss_link,
            label=label
        )
        self.db.add(topic)
        self.db.commit()
        self.db.refresh(topic)
        return topic

    def get_topic_by_id(self, topic_id: int):
        return self.db.query(Topic).filter(Topic.id == topic_id).first()
    
    def get_all_topics(self):
        return self.db.query(Topic).all()