from datetime import datetime

from sqlalchemy.orm import Session

from news_anchor.models.topic_model import Topic
from news_anchor.models.user_model import User
from news_anchor.models.user_topics_model import UserTopics


class UserRepository:

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def create_user(self, name: str, username: str, email: str, password: str):
        user = User(name=name, username=username, email=email, password=password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def get_all_users(self):
        return self.db.query(User).all()

    def get_user_topics(self, user_id: int):
        return (
            self.db.query(
                UserTopics.user_id,
                Topic.id.label("topic_id"),
                Topic.rss_link,
                Topic.label,
            )
            .join(Topic, UserTopics.topic_id == Topic.id)
            .filter(UserTopics.user_id == user_id)
            .all()
        )

    def add_user_topic(self, user_id: int, topic_id: int):
        user_topic = UserTopics(
            user_id=user_id, topic_id=topic_id, created_at=datetime.utcnow()
        )
        self.db.add(user_topic)
        self.db.commit()
        self.db.refresh(user_topic)
        return user_topic
