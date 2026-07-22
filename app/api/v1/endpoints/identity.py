"""
Identity API Endpoints

Purpose:
- Expose REST endpoints for ServiceNow identity management.
- Verify platform user identity against ServiceNow.
"""

from uuid import UUID

from fastapi import APIRouter, Depends

from app.api.dependencies.auth import get_current_user_id
from app.api.dependencies.identity import get_identity_service
from app.application.identity.responses import VerifyIdentityResponse
from app.application.identity.service import IdentityService
from app.core.logging import get_logger

logger = get_logger(__name__)

# ============================================================
# Router
# ============================================================

router = APIRouter(
    prefix="/identity",
    tags=["Identity"],
)

# ============================================================
# Verify Identity
# ============================================================


@router.post(
    "/verify",
    response_model=VerifyIdentityResponse,
    summary="Verify ServiceNow Identity",
    description="Verify the authenticated platform user's identity against ServiceNow.",
)
async def verify_identity(
    current_user_id: UUID = Depends(
        get_current_user_id,
    ),
    service: IdentityService = Depends(
        get_identity_service,
    ),
) -> VerifyIdentityResponse:
    """
    Verify the authenticated user's
    ServiceNow identity.
    """

    logger.info(
        "Received identity verification request.",
    )

    response = await service.verify_identity(
        current_user_id,
    )

    logger.info(
        "Identity verification completed for user %s.",
        current_user_id,
    )

    return response
