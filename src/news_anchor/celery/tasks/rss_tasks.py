import json
import logging
from datetime import datetime

from sqlalchemy.orm.session import Session

from news_anchor.celery.celery_worker import celery
from news_anchor.celery.rss.rss_fetcher import rss_to_json
from news_anchor.database.database import SessionLocal
from news_anchor.schemas.articles_schema import AddArticleSchema
from news_anchor.services.articles_service import ArticlesService
from news_anchor.services.topics_service import TopicsService

logger = logging.getLogger(__name__)


@celery.task(bind=True)
def fetch_news(self):
    """Fetch news from RSS feeds for all topics"""
    db = None
    try:
        db = SessionLocal()

        topics_with_rss_links = _get_all_rss_links(db)

        if not topics_with_rss_links:
            logger.info("No topics found with RSS links")
            return "No topics to process"

        successful_fetches = 0
        failed_fetches = 0

        for topic in topics_with_rss_links:
            try:
                if not hasattr(topic, "rss_link") or not topic.rss_link:
                    logger.warning(
                        f"Topic {topic.id if hasattr(topic, 'id') else 'unknown'} has no RSS link"
                    )
                    failed_fetches += 1
                    continue

                logger.info(f"Fetching RSS data for topic: {topic.rss_link}")
                rss_data_json = rss_to_json(topic.rss_link)

                # Parse the JSON string and add articles to database
                articles_added = _add_news_to_database(db, rss_data_json, topic.id)

                logger.info(
                    f"Successfully fetched and added {articles_added} articles for {topic.rss_link}"
                )
                successful_fetches += 1

            except Exception as e:
                logger.error(f"Failed to fetch RSS data for {topic.rss_link}: {str(e)}")
                failed_fetches += 1

        result = f"RSS fetch completed: {successful_fetches} successful, {failed_fetches} failed"
        logger.info(result)
        return result

    except Exception as e:
        logger.error(f"Failed to fetch news: {str(e)}")
        # Retry the task if it fails
        raise self.retry(exc=e, countdown=60, max_retries=3)

    finally:
        # Always close the database session
        if db:
            db.close()


def _get_all_rss_links(db: Session):
    """Get all RSS links from database - internal helper function"""
    try:
        topics_service = TopicsService(db)
        topics_with_rss_links = topics_service.get_all_topics()
        return topics_with_rss_links
    except Exception as e:
        logger.error(f"Failed to get RSS links from database: {str(e)}")
        raise


def _add_news_to_database(db: Session, rss_json_data: str, topic_id: int) -> int:
    """Add news articles to database from RSS JSON data"""
    try:
        # Parse the JSON string returned by rss_to_json
        rss_data = json.loads(rss_json_data)
        articles_service = ArticlesService(db)
        articles_added = 0

        # Process each entry in the RSS feed
        for entry in rss_data.get("entries", []):
            try:
                # Parse the published date if available
                published_at = datetime.strptime(
                    entry.get("published_at"), "%Y-%m-%dT%H:%M:%S%z"
                )
                current_date = datetime.utcnow().date()

                logger.info(
                    f"Published at: {published_at.date()}, current date: {datetime.utcnow().date()}"
                )

                if published_at.date() == current_date and articles_added < 10:
                    try:
                        # Create the article schema with proper mapping
                        article_data = AddArticleSchema(
                            title=entry.get("title", ""),
                            link=entry.get("link", ""),
                            image=entry.get("image"),  # This is already Optional
                            summary=entry.get("summary", ""),
                            topic_id=topic_id,  # This is the crucial missing piece!
                            published_at=published_at,
                            created_at=datetime.utcnow(),
                        )

                        # Check if article already exists (avoid duplicates)
                        # You might want to add a method in ArticlesService to check for existing articles by link
                        articles_service.add_article(article_data)
                        articles_added += 1

                    except Exception as date_e:
                        logger.warning(
                            f"Failed to parse date '{entry.get('published_at')}': {str(date_e)}"
                        )

            except Exception as article_e:
                logger.error(f"Failed to process individual article: {str(article_e)}")
                continue  # Skip this article but continue with others

        logger.info(f"Successfully added {articles_added} articles to database")
        return articles_added

    except json.JSONDecodeError as json_e:
        logger.error(f"Failed to parse RSS JSON data: {str(json_e)}")
        raise
    except Exception as e:
        logger.error(f"Failed to add articles to database: {str(e)}")
        raise
