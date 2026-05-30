from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from news_anchor.schemas.user_schema import UserResponseSchema, UserTopicsResponseSchema
from news_anchor.services.user_service import UserService
from news_anchor.database.database import get_db

router = APIRouter()

@router.get("/all", response_model=list[UserResponseSchema])
def get_all_users(db: Session = Depends(get_db)):
    """List all users"""
    user_service = UserService(db)
    users = user_service.get_all_users()
    return users

@router.get("/get-user-topics", response_model=list[UserTopicsResponseSchema])
def get_user_topics(user_id: int, db: Session = Depends(get_db)):
    """Get topics for user"""
    user_service = UserService(db)
    topics = user_service.get_user_topics(user_id)
    return topics