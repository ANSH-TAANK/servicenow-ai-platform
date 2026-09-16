"""
Approval Integration Service

Purpose:
- Coordinate approval creation between PostgreSQL
  and ServiceNow.
- Preserve eventual consistency.
- Synchronize local approval records with
  ServiceNow approval requests.

This module DOES NOT:
- Contain approval business rules.
- Access repositories directly.
- Expose API routes.
"""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.application.approval.service import ApprovalService
from app.core.logging import get_logger
from app.infrastructure.database.models.user_approval import UserApproval
from app.infrastructure.servicenow.approval_service import ServiceNowApprovalService
from app.infrastructure.servicenow.client import ServiceNowClient
from app.infrastructure.servicenow.models import ApprovalRequestCreate, ServiceNowUser

logger = get_logger(__name__)


# ============================================================
# Approval Integration Service
# ============================================================


class ApprovalIntegrationService:
    """
    Coordinates approval synchronization between
    PostgreSQL and ServiceNow.
    """

    # ============================================================
    # Constructor
    # ============================================================

    def __init__(
        self,
        db: AsyncSession,
    ) -> None:
        """
        Initialize integration services.
        """

        self._approval_service = ApprovalService(db)

        client = ServiceNowClient()

        self._servicenow = ServiceNowApprovalService(
            client=client,
        )

    # ============================================================
    # Public Methods
    # ============================================================

    async def create_manual_approval(
        self,
        *,
        user_id: UUID,
        full_name: str,
        username: str,
        email: str,
        access_justification: str | None = None,
    ) -> UserApproval:
        """
        Create a local approval record and
        synchronize it with ServiceNow.
        """

        logger.info(
            "Creating manual approval for user %s.",
            user_id,
        )

        first_name, last_name = self._split_full_name(
            full_name,
        )

        approval = await self._approval_service.create_manual_approval(
            user_id=user_id,
        )

        try:
            logger.info(
                "Creating ServiceNow approval request for user %s.",
                user_id,
            )

            request = ApprovalRequestCreate(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                fastapi_user_id=str(user_id),
                access_justification=access_justification,
            )

            response = self._servicenow.create_request(
                request,
            )

            approval = await self._approval_service.update_servicenow_reference(
                approval=approval,
                sys_id=response.sys_id,
                number=response.number,
            )

            logger.info(
                "Approval synchronized successfully for user %s.",
                user_id,
            )

        except Exception as exc:
            logger.exception(
                "Failed to synchronize approval with ServiceNow for user %s.",
                user_id,
            )

            approval = await self._approval_service.mark_servicenow_sync_failed(
                approval=approval,
                error=str(exc),
            )

        return approval

    async def create_auto_approval(
        self,
        *,
        user_id: UUID,
    ) -> UserApproval:
        """
        Create an automatically approved record
        for an existing ServiceNow user.
        """

        logger.info(
            "Creating auto approval for user %s.",
            user_id,
        )

        return await self._approval_service.create_auto_approval(
            user_id=user_id,
        )

    async def retry_failed_sync(
        self,
        approval: UserApproval,
        *,
        full_name: str,
        username: str,
        email: str,
        access_justification: str | None = None,
    ) -> UserApproval:
        """
        Retry synchronization with ServiceNow.
        """

        logger.info(
            "Retrying ServiceNow synchronization for approval %s.",
            approval.id,
        )

        first_name, last_name = self._split_full_name(
            full_name,
        )

        approval = await self._approval_service.mark_servicenow_retrying(
            approval,
        )

        try:
            request = ApprovalRequestCreate(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                fastapi_user_id=str(approval.user_id),
                access_justification=access_justification,
            )

            response = self._servicenow.create_request(
                request,
            )

            approval = await self._approval_service.update_servicenow_reference(
                approval=approval,
                sys_id=response.sys_id,
                number=response.number,
            )

            logger.info(
                "Retry synchronization successful for approval %s.",
                approval.id,
            )

        except Exception as exc:
            logger.exception(
                "Retry synchronization failed for approval %s.",
                approval.id,
            )

            approval = await self._approval_service.mark_servicenow_sync_failed(
                approval=approval,
                error=str(exc),
            )

        return approval

    def find_servicenow_user(
        self,
        *,
        email: str,
    ) -> ServiceNowUser | None:
        """
        Find a ServiceNow user by email.
        """

        logger.info(
            "Looking up ServiceNow user with email '%s'.",
            email,
        )

        return self._servicenow.find_user_by_email(
            email,
        )

    # ============================================================
    # Private Methods
    # ============================================================

    def _split_full_name(
        self,
        full_name: str,
    ) -> tuple[str, str]:
        """
        Split a full name into first and last name.

        If only one name is provided, the last name
        will be an empty string.
        """

        parts = full_name.strip().split(maxsplit=1)

        if not parts:
            return "", ""

        first_name = parts[0]
        last_name = parts[1] if len(parts) > 1 else ""

        return first_name, last_name
