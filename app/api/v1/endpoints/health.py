"""
Health Endpoints

Purpose:
- Expose application health endpoints.
"""

from fastapi import APIRouter

from app.core.config import settings
from app.schemas.health import HealthResponse

# ============================================================
# Health Router
# ============================================================

router = APIRouter()


# ============================================================
# Health Check
# ============================================================


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Application Health Check",
)
async def get_health() -> HealthResponse:
    """
    Return the current health status
    of the application.
    """

    return HealthResponse(
        status="healthy",
        application=settings.application.name,
        version=settings.application.version,
    )
