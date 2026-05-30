from fastapi import APIRouter


router = APIRouter()

@router.get('/get-news-from-rss')
def get_news_from_rss():
    """ Get news from RSS """

    return {"data": "News from RSS"}

