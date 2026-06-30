"""
Root API Router

Purpose:
- Register all API versions.
- Expose a single router to the application.
"""

from fastapi import APIRouter

from app.api.v1.router import router as v1_router

# ============================================================
# Root API Router
# ============================================================

router = APIRouter()

router.include_router(
    v1_router,
)
