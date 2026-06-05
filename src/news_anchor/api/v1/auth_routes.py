from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.session import Session

from news_anchor.database.database import get_db
from news_anchor.schemas.auth_schema import (AuthResponseSchema,
                                             LoginUserSchema,
                                             RegisterUserSchema)
from news_anchor.services.user_service import UserService

router = APIRouter()


@router.post("/login", response_model=AuthResponseSchema)
def login(login_data: LoginUserSchema, db: Session = Depends(get_db)):
    """Login"""

    try:
        user_service = UserService(db)
        auth_response = user_service.login_user(login_data)
        return auth_response
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/register", response_model=AuthResponseSchema)
def register(register_data: RegisterUserSchema, db: Session = Depends(get_db)):
    """Register"""

    user_service = UserService(db)
    auth_response = user_service.register_user(register_data)

    if not auth_response:
        raise HTTPException(status_code=400, detail="Failed to register user")

    return auth_response
