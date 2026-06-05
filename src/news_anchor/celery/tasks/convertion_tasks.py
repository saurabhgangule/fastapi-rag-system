import logging
import time
from asyncio import run

import edge_tts
from sqlalchemy.orm.session import Session

from news_anchor.celery.celery_worker import celery
from news_anchor.database.database import SessionLocal
from news_anchor.services.broadcasts_service import BroadcastsService
from news_anchor.services.groq_service import GroqService

logger = logging.getLogger(__name__)


@celery.task(bind=True, max_retries=3)
def convert_summaries_to_mp3(self):
    """Convert summaries to mp3"""

    try:
        logger.info("Starting summaries to mp3 conversion task")

        handle_convert_summaries_to_mp3()

        logger.info("Summaries to mp3 conversion task completed successfully")

    except Exception as e:
        logger.error(f"Summaries to mp3 conversion task failed: {str(e)}")

        # Retry task after 60 seconds
        raise self.retry(exc=e, countdown=60)


def handle_convert_summaries_to_mp3():
    """Convert summaries to mp3"""

    groq_service = GroqService()

    db = SessionLocal()

    try:
        broadcasts = _get_all_broadcasts_to_convert(db)

        logger.info(f"Found {len(broadcasts)} broadcasts to convert")

        for broadcast in broadcasts:

            try:
                logger.info(f"Converting broadcast {broadcast.id} to mp3")

                # broadcast_mp3_url = groq_service.convert_summary_to_mp3(broadcast.broadcast_summary)
                broadcast_mp3_url = run(
                    groq_service.convert_summary_to_mp3_using_edge_tts(
                        broadcast.broadcast_summary
                    )
                )

                time.sleep(2)

                logger.info(f"Broadcast {broadcast.id} converted to mp3 successfully")

                _save_broadcast_mp3_url_to_database(db, broadcast.id, broadcast_mp3_url)

                logger.info(
                    f"Broadcast {broadcast.id} mp3 url saved to database successfully"
                )

            except Exception as e:
                logger.error(
                    f"Failed to convert broadcast {broadcast.id} to mp3: {str(e)}"
                )
                continue

    except Exception as broadcast_error:
        logger.error(f"Failed to convert summaries to mp3: {str(broadcast_error)}")
        raise

    finally:
        db.close()


def _get_all_broadcasts_to_convert(db: Session):
    """Get all broadcasts to convert"""

    try:
        broadcasts_service = BroadcastsService(db)
        return broadcasts_service.get_all_broadcasts()
    except Exception as e:
        logger.error(f"Failed to get all broadcasts to convert: {str(e)}")
        raise


def _save_broadcast_mp3_url_to_database(
    db: Session, broadcast_id: int, broadcast_mp3_url: str
):
    """Save broadcast mp3 url to database"""

    try:
        broadcasts_service = BroadcastsService(db)
        return broadcasts_service.save_broadcast_mp3_url(
            broadcast_id, broadcast_mp3_url
        )
    except Exception as e:
        logger.error(f"Failed to save broadcast mp3 url to database: {str(e)}")
        raise
