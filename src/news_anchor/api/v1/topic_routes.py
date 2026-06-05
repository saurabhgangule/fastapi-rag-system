from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from news_anchor.database.database import get_db
from news_anchor.schemas.topics_schema import TopicResponseSchema
from news_anchor.services.topics_service import TopicsService

router = APIRouter()


@router.get("/all", response_model=list[TopicResponseSchema])
def get_topics(db: Session = Depends(get_db)):
    """Get topics list"""

    topics_service = TopicsService(db)
    topics = topics_service.get_all_topics()
    return topics
