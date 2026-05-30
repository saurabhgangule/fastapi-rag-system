from sqlalchemy.orm import Session
from news_anchor.repositories.user_repository import UserRepository
from news_anchor.schemas.user_schema import CreateUserSchema

class UserService:

    def __init__(self, db: Session) -> None:
        self.user_repository = UserRepository(db)
        
    def create_user(self, user_data: CreateUserSchema):

        existing_user = self.user_repository.get_user_by_email(
            user_data.email
        )

        if existing_user:
            raise Exception("Email already exists")

        return self.user_repository.create_user(
            username = user_data.username,
            email = user_data.email
        )

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