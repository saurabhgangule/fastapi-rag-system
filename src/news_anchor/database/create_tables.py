"""Create database tables."""

from news_anchor.database.database import engine
from news_anchor.models.user_model import Base

def create_tables():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")

if __name__ == "__main__":
    create_tables()