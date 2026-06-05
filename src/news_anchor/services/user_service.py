from sqlalchemy.orm import Session

from news_anchor.repositories.user_repository import UserRepository
from news_anchor.schemas.auth_schema import LoginUserSchema, RegisterUserSchema
from news_anchor.services.jwt_service import (check_password,
                                              create_access_token,
                                              hash_password)


class UserService:

    def __init__(self, db: Session) -> None:
        self.user_repository = UserRepository(db)

    def register_user(self, user_data: RegisterUserSchema):
        existing_user = self.user_repository.get_user_by_email(user_data.email)
        if existing_user:
            raise Exception("Email already exists")

        user = self.user_repository.create_user(
            name=user_data.name,
            username=user_data.username,
            email=user_data.email,
            password=hash_password(user_data.password),
        )
        if not user:
            raise Exception("Failed to create user")

        token = create_access_token(user.id)

        return {"access_token": token, "token_type": "Bearer"}

    def login_user(self, login_data: LoginUserSchema):
        user = self.user_repository.get_user_by_email(login_data.email)
        if not user:
            raise Exception("User not found")
        if not check_password(login_data.password, user.password):
            raise Exception("Invalid password")

        token = create_access_token(user.id)

        return {"access_token": token, "token_type": "Bearer"}

    def get_user(self, user_id: int):
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise Exception("User not found")

        return user

    def get_all_users(self):
        users = self.user_repository.get_all_users()
        if not users:
            raise Exception("Users not found")

        return users

    def get_user_topics(self, user_id: int):
        user_topics = self.user_repository.get_user_topics(user_id)
        if not user_topics:
            raise Exception("User topics not found")

        return user_topics

    def add_user_topic(self, user_id: int, topic_id: int):
        """Add a single topic to user"""

        # Check if user exists
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise Exception("User not found")

        # Get current user topics once
        current_user_topics = self.user_repository.get_user_topics(user_id)
        current_topic_ids = {
            topic.topic_id for topic in current_user_topics
        }  # Use set for O(1) lookup

        # Check if topic already exists
        if topic_id in current_topic_ids:
            raise Exception("Topic already added to user")

        # Add the topic
        user_topic = self.user_repository.add_user_topic(user_id, topic_id)
        if not user_topic:
            raise Exception("Failed to add topic to user")

        return user_topic

    def add_user_topics_bulk(self, user_id: int, topic_ids: list[int]):
        """Add multiple topics to user (bulk operation)"""

        # Check if user exists
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise Exception("User not found")

        # Get current user topics once
        current_user_topics = self.user_repository.get_user_topics(user_id)
        current_topic_ids = {topic.topic_id for topic in current_user_topics}

        added_topics = []
        skipped_topics = []
        failed_topics = []

        for topic_id in topic_ids:
            if topic_id in current_topic_ids:
                skipped_topics.append(topic_id)
                continue

            try:
                user_topic = self.user_repository.add_user_topic(user_id, topic_id)
                if user_topic:
                    added_topics.append(topic_id)
                    current_topic_ids.add(
                        topic_id
                    )  # Update set to avoid duplicate attempts
                else:
                    failed_topics.append(topic_id)
            except Exception as e:
                failed_topics.append(topic_id)

        return {
            "added_count": len(added_topics),
            "skipped_count": len(skipped_topics),
            "failed_count": len(failed_topics),
            "added_topics": added_topics,
            "skipped_topics": skipped_topics,
            "failed_topics": failed_topics,
        }
