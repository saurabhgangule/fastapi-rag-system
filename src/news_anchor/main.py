"""Main FastAPI application entry point."""

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()


# from news_anchor.api.middleware import add_middleware
# from news_anchor.api.exception_handlers import add_exception_handlers
from news_anchor.api.v1 import news_routes, broadcast_routes, topic_routes, health_routes, user_routes
# from news_anchor.core.config import settings
# from news_anchor.core.logger import logger
from news_anchor.database.database import get_db

get_db()




def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    
    app = FastAPI(
        title=os.getenv("PROJECT_NAME"),
        description=os.getenv("PROJECT_DESCRIPTION"),
        version=os.getenv("VERSION"),
        openapi_url=f"{os.getenv("API_V1_STR")}/openapi.json",
        docs_url=f"{os.getenv("API_V1_STR")}/docs",
        redoc_url=f"{os.getenv("API_V1_STR")}/redoc",
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=os.getenv("BACKEND_CORS_ORIGINS"),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add custom middleware
    # add_middleware(app)
    
    # Add exception handlers
    # add_exception_handlers(app)

    # Include routers
    app.include_router(health_routes.router, prefix=f"{os.getenv("API_V1_STR")}/health", tags=["health"])
    app.include_router(news_routes.router, prefix=f"{os.getenv("API_V1_STR")}/news", tags=["news"])
    app.include_router(broadcast_routes.router, prefix=f"{os.getenv("API_V1_STR")}/broadcasts", tags=["broadcasts"])
    app.include_router(topic_routes.router, prefix=f"{os.getenv("API_V1_STR")}/topics", tags=["Topics"], dependencies=[Depends(get_db)])
    app.include_router(user_routes.router, prefix=f"{os.getenv("API_V1_STR")}/users", tags=["Users"], dependencies=[Depends(get_db)])

    # logger.info("FastAPI application created successfully")
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )