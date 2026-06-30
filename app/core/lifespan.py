"""
Application Lifespan

Purpose:
- Manage application startup.
- Manage application shutdown.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.logging import get_logger

logger = get_logger(__name__)

# ============================================================
# Application Lifespan
# ============================================================


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage the application's startup
    and shutdown lifecycle.
    """

    logger.info("Starting ServiceNow AI Platform.")

    yield

    logger.info("Shutting down ServiceNow AI Platform.")
