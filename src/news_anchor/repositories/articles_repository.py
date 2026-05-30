from sqlalchemy.orm import Session
from news_anchor.models.article_model import Article
from news_anchor.models.user_topics_model import UserTopics
from news_anchor.schemas.articles_schema import AddArticleSchema

class ArticlesRepository:

    def __init__(self, db: Session) -> None:
        self.db = db

    def add_article(self, article_data: AddArticleSchema):
        article = Article(
            title=article_data.title,
            link=article_data.link,
            image=article_data.image,
            summary=article_data.summary,
            topic_id=article_data.topic_id,
            published_at=article_data.published_at
        )
        self.db.add(article)
        self.db.commit()
        self.db.refresh(article)
        return article

    def get_article_by_id(self, article_id: int):
        return self.db.query(Article).filter(Article.id == article_id).first()
    
    def get_all_articles(self):
        return self.db.query(Article).all()

    def get_articles_by_topic_id(self, topic_id: int):
        return self.db.query(Article).filter(Article.topic_id == topic_id).all()

    def get_article_by_link(self, link: str):
        return self.db.query(Article).filter(Article.link == link).first()

    def get_articles_by_user_id(self, user_id: int):
        return self.db.query(
            Article.id,
            Article.title,
            Article.link,
            Article.image,
            Article.summary,
            Article.topic_id,
            Article.published_at,
            Article.created_at
        ).join(UserTopics, Article.topic_id == UserTopics.topic_id).filter(UserTopics.user_id == user_id).all()