"""
Approval API Endpoints

Purpose:
- Receive approval callbacks from ServiceNow.
- Delegate callback processing to the ApprovalService.

This module DOES NOT:
- Contain business logic.
- Access the database directly.
"""

from fastapi import APIRouter, Depends, status

from app.api.dependencies.approval import get_approval_service
from app.api.dependencies.webhook_auth import verify_webhook
from app.application.approval.requests import ApprovalCallbackRequest
from app.application.approval.responses import ApprovalCallbackResponse
from app.application.approval.service import ApprovalService
from app.core.constants import APPROVAL_CALLBACK_SUCCESS_MESSAGE
from app.core.logging import get_logger

logger = get_logger(__name__)

# ============================================================
# Router
# ============================================================

router = APIRouter(
    prefix="/servicenow",
    tags=["ServiceNow"],
)


# ============================================================
# Approval Callback
# ============================================================


@router.post(
    "/callback",
    response_model=ApprovalCallbackResponse,
    status_code=status.HTTP_200_OK,
    summary="Approval Callback",
    description="Receive approval callbacks from ServiceNow.",
)
async def approval_callback(
    request: ApprovalCallbackRequest,
    _: None = Depends(
        verify_webhook,
    ),
    service: ApprovalService = Depends(
        get_approval_service,
    ),
) -> ApprovalCallbackResponse:
    """
    Process an approval callback from ServiceNow.
    """

    logger.info(
        "Received approval callback for user %s.",
        request.fastapi_user_id,
    )

    await service.process_callback(
        request,
    )

    logger.info(
        "Approval callback processed successfully for user %s.",
        request.fastapi_user_id,
    )

    return ApprovalCallbackResponse(
        message=APPROVAL_CALLBACK_SUCCESS_MESSAGE,
    )
