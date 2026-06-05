import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from news_anchor.database.database import get_db
from news_anchor.schemas.user_schema import (UserResponseSchema,
                                             UserTopicsResponseSchema)
from news_anchor.services.user_service import UserService
from news_anchor.utils.auth_dependency import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/all", response_model=list[UserResponseSchema])
def get_all_users(db: Session = Depends(get_db)):
    """List all users"""

    user_service = UserService(db)
    users = user_service.get_all_users()
    return users


@router.get("/topics", response_model=list[UserTopicsResponseSchema])
def get_user_topics(
    db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user)
):
    """Get topics for user"""

    try:
        user_service = UserService(db)
        topics = user_service.get_user_topics(current_user_id)
        return topics
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Failed to get user topics: {str(e)}"
        )


@router.post("/topics")
def add_user_topic(
    topic_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user),
):
    """Add topic to current user"""

    try:
        user_service = UserService(db)
        user_topic = user_service.add_user_topic(current_user_id, topic_id)
        return {
            "success": True,
            "message": "Topic added successfully",
            "user_topic": user_topic,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/topics/bulk")
def add_user_topics_bulk(
    topic_ids: list[int],
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user),
):
    """Add multiple topics to current user"""

    try:
        user_service = UserService(db)
        result = user_service.add_user_topics_bulk(current_user_id, topic_ids)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
