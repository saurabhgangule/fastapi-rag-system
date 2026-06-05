import logging
import time
from datetime import datetime

from sqlalchemy.orm import Session

from news_anchor.celery.celery_worker import celery
from news_anchor.database.database import SessionLocal
from news_anchor.schemas.broadcasts_schema import AddBroadcastSchema
from news_anchor.services.articles_service import ArticlesService
from news_anchor.services.broadcasts_service import BroadcastsService
from news_anchor.services.groq_service import GroqService
from news_anchor.services.user_service import UserService

logger = logging.getLogger(__name__)


@celery.task(bind=True, max_retries=3)
def broadcast_news(self):
    """
    Broadcast summarized news to all users.
    """
    try:
        logger.info("Starting news broadcast task")

        handle_broadcast_news()

        logger.info("News broadcast task completed successfully")

    except Exception as e:
        logger.error(f"Broadcast task failed: {str(e)}")

        # Retry task after 60 seconds
        raise self.retry(exc=e, countdown=60)


def handle_broadcast_news():
    """
    Main broadcast processing logic.

    Flow:
    1. Fetch all users
    2. Fetch articles for each user
    3. Generate AI summary
    4. Save broadcast to DB
    """

    groq_service = GroqService()
    db = SessionLocal()

    try:
        users = _get_all_users_to_broadcast(db)
        logger.info(f"Found {len(users)} users for broadcasting")

        for user in users:

            try:
                logger.info(f"Processing user: {user.id}")
                articles = _get_articles_to_broadcast(db=db, user_id=user.id)

                if not articles:
                    logger.info(f"No articles found for user {user.id}")
                    continue

                user_articles = []
                articles = articles[:10]

                for article in articles:
                    if article.summary:
                        user_articles.append(article.summary)

                        logger.info(
                            f"Adding article for user {user.id}: " f"{article.title}"
                        )

                if not user_articles:
                    logger.info(f"No article summaries available for user {user.id}")
                    continue

                articles_content = "\n".join(user_articles)
                articles_content = articles_content[:12000]

                logger.info(f"Generating AI summary for user {user.id}")

                broadcast_summary = groq_service.summarize_text(
                    user.username, articles_content
                )

                # =========================================
                # Optional throttling
                # Helps avoid:
                # - Groq rate limits
                # - API burst failures
                # =========================================
                time.sleep(2)

                _save_broadcast_to_database(
                    db=db,
                    user_id=user.id,
                    broadcast_summary=broadcast_summary,
                    broadcast_mp3_url=None,
                    broadcasted_at=datetime.utcnow(),
                )

                logger.info(f"Broadcast saved successfully for user {user.id}")

            except Exception as user_error:
                logger.error(f"Failed processing user {user.id}: " f"{str(user_error)}")
                continue

    finally:
        # Always close DB session
        db.close()


def _get_all_users_to_broadcast(db: Session):
    """
    Fetch all users eligible for broadcast.
    """

    try:
        users_service = UserService(db)
        return users_service.get_all_users()

    except Exception as e:
        logger.error(f"Failed to fetch users: {str(e)}")
        raise


def _get_articles_to_broadcast(db: Session, user_id: int):
    """
    Fetch articles relevant to user.
    """

    try:
        articles_service = ArticlesService(db)
        return articles_service.get_articles_by_user_id(user_id)

    except Exception as e:
        logger.error(f"Failed fetching articles for user {user_id}: {str(e)}")
        raise


def _save_broadcast_to_database(
    db: Session,
    user_id: int,
    broadcast_summary: str,
    broadcast_mp3_url: str | None,
    broadcasted_at: datetime,
):
    """
    Save generated broadcast into DB.
    """

    try:
        broadcasts_service = BroadcastsService(db)
        broadcasts_service.add_broadcast(
            AddBroadcastSchema(
                user_id=user_id,
                broadcast_summary=broadcast_summary,
                broadcast_mp3_url=broadcast_mp3_url,
                broadcasted_at=broadcasted_at,
            )
        )

    except Exception as e:
        logger.error(f"Failed saving broadcast for user {user_id}: {str(e)}")
        raise
