"""
API Version 1 Router

Purpose:
- Register all Version 1 endpoints.
"""

from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.identity import router as identity_router
from app.api.v1.endpoints.incident import router as incident_router

# ============================================================
# Version 1 Router
# ============================================================

router = APIRouter(
    prefix="/api/v1",
)

router.include_router(
    health_router,
)

router.include_router(
    incident_router,
)

router.include_router(
    auth_router,
)

router.include_router(
    identity_router,
)
