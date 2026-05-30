from sqlalchemy.orm import Session
from news_anchor.repositories.articles_repository import ArticlesRepository
from news_anchor.schemas.articles_schema import AddArticleSchema

class ArticlesService:

    def __init__(self, db: Session) -> None:
        self.articles_repository = ArticlesRepository(db)

    def add_article(self, article_data: AddArticleSchema):
        existing_article = self.articles_repository.get_article_by_link(article_data.link)

        if existing_article:
            return True

        return self.articles_repository.add_article(article_data)

    def get_all_articles(self):
        return self.articles_repository.get_all_articles()

    def get_articles_by_topic_id(self, topic_id: int):
        return self.articles_repository.get_articles_by_topic_id(topic_id)

    def get_articles_by_user_id(self, user_id: int):
        return self.articles_repository.get_articles_by_user_id(user_id)