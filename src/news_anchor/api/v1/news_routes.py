from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.session import Session

from news_anchor.database.database import get_db
from news_anchor.schemas.articles_schema import ArticleSchema
from news_anchor.services.articles_service import ArticlesService
from news_anchor.utils.auth_dependency import get_current_user

router = APIRouter()


@router.get("/personalized", response_model=List[ArticleSchema])
def get_personalized_news(
    db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user)
):
    """Get personalized news articles for current user"""

    try:
        articles_service = ArticlesService(db)
        news_articles = articles_service.get_articles_by_user_id(current_user_id)
        return news_articles
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
