from fastapi import APIRouter


router = APIRouter()

@router.get('/')
def get_health():
    """ Health check """

    return {"data": "Healthy"}

