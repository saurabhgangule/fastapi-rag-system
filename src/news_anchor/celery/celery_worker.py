import os

from celery import Celery
from dotenv import load_dotenv

load_dotenv()

celery = Celery(
    "news_anchor",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_RESULT_BACKEND"),
)

celery.conf.timezone = "UTC"

celery.autodiscover_tasks(
    [
        "news_anchor.celery.tasks",
    ]
)


# import news_anchor.celery.tasks.rss_tasks
# celery.conf.beat_schedule = {
#     "fetch-news-every-1-minute": {
#         "task": "news_anchor.celery.tasks.rss_tasks.fetch_news",
#         "schedule": 60.0,
#     },
# }

import news_anchor.celery.tasks.broadcast_tasks
import news_anchor.celery.tasks.convertion_tasks

celery.conf.beat_schedule = {
    # "broadcast-news-every-1-minute": {
    #     "task": "news_anchor.celery.tasks.broadcast_tasks.broadcast_news",
    #     "schedule": 60.0,
    # },
    "convert-summaries-to-mp3-every-1-minute": {
        "task": "news_anchor.celery.tasks.convertion_tasks.convert_summaries_to_mp3",
        "schedule": 60.0,
    },
}
