from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.session import Session

from news_anchor.database.database import get_db
from news_anchor.schemas.broadcasts_schema import BroadcastResponseSchema
from news_anchor.services.broadcasts_service import BroadcastsService
from news_anchor.utils.auth_dependency import get_current_user

router = APIRouter()


@router.get("/history", response_model=List[BroadcastResponseSchema])
def get_broadcast_history(
    db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user)
):
    """Get broadcast history for current user"""

    try:
        broadcasts_service = BroadcastsService(db)
        broadcast_history = broadcasts_service.get_broadcast_history(current_user_id)
        return broadcast_history
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/today", response_model=BroadcastResponseSchema)
def get_today_broadcast(
    db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user)
):
    """Get today's broadcast for current user"""

    try:
        broadcasts_service = BroadcastsService(db)
        todays_broadcast = broadcasts_service.get_todays_broadcast(current_user_id)
        return todays_broadcast
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
