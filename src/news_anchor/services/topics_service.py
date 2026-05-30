from sqlalchemy.orm import Session
from news_anchor.repositories.topics_repository import TopicsRepository
from news_anchor.schemas.topics_schema import AddTopicSchema

class TopicsService:

    def __init__(self, db: Session) -> None:
        self.topics_repository = TopicsRepository(db)

    def add_topic(self, topic_data: AddTopicSchema):
        existing_topic = self.topics_repository.get_topic_by_rss_link(topic_data.rss_link)

        if existing_topic:
            return True

        return self.topics_repository.add_topic(topic_data)

    def get_all_topics(self):
        return self.topics_repository.get_all_topics()

    def get_topic_by_id(self, topic_id: int):
        return self.topics_repository.get_topic_by_id(topic_id)