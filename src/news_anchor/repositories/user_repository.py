from sqlalchemy.orm import Session
from news_anchor.models.user_model import User
from news_anchor.models.user_topics_model import UserTopics
from news_anchor.models.topic_model import Topic

class UserRepository:

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def create_user(self, username: str, email: str):
        user = User(
            username=username,
            email=email
        )
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
        return self.db.query(
            UserTopics.user_id,
            Topic.id.label("topic_id"),
            Topic.rss_link,
            Topic.label
        ).join(Topic, UserTopics.topic_id == Topic.id).filter(UserTopics.user_id == user_id).all()