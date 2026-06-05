"""Main FastAPI application entry point."""

import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from news_anchor.api.v1 import (auth_routes, broadcast_routes, health_routes,
                                news_routes, topic_routes, user_routes)
from news_anchor.database.database import get_db
from news_anchor.utils.auth_dependency import get_current_user

load_dotenv()
get_db()


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""

    API_V1_STR = os.getenv("API_V1_STR")

    app = FastAPI(
        debug=True,
        title=os.getenv("PROJECT_NAME"),
        description=os.getenv("PROJECT_DESCRIPTION"),
        version=os.getenv("VERSION"),
        openapi_url=f"{API_V1_STR}/openapi.json",
        docs_url=f"{API_V1_STR}/docs",
        redoc_url=f"{API_V1_STR}/redoc",
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=os.getenv("BACKEND_CORS_ORIGINS"),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(
        health_routes.router,
        prefix=f"{API_V1_STR}/health",
        tags=["Health Check"],
    )
    app.include_router(
        auth_routes.router,
        prefix=f"{API_V1_STR}/auth",
        tags=["Authentication"],
        dependencies=[Depends(get_db)],
    )
    app.include_router(
        news_routes.router, prefix=f"{API_V1_STR}/news", tags=["News Articles"]
    )
    app.include_router(
        broadcast_routes.router,
        prefix=f"{API_V1_STR}/broadcasts",
        tags=["News Broadcasts"],
    )
    app.include_router(
        topic_routes.router,
        prefix=f"{API_V1_STR}/topics",
        tags=["News Topics"],
        dependencies=[Depends(get_db)],
    )
    app.include_router(
        user_routes.router,
        prefix=f"{API_V1_STR}/user",
        tags=["Users"],
        dependencies=[Depends(get_db), Depends(get_current_user)],
    )

    # logger.info("FastAPI application created successfully")
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
