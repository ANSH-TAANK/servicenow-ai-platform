"""
Approval Service

Purpose:
- Handle user approval business logic.
- Coordinate approval repositories.
- Determine whether users are allowed to access the platform.

This module DOES NOT:
- Define API routes.
- Access HTTP requests directly.
- Call ServiceNow APIs.
"""

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.application.approval.exceptions import (
    ApprovalAlreadyProcessedError,
    ApprovalNotFoundError,
    InvalidApprovalCallbackError,
)
from app.application.approval.requests import ApprovalCallbackRequest
from app.core.constants import (  # REJECTED_CALLBACK_MISSING_REASON_MESSAGE,
    APPROVED_CALLBACK_MISSING_USER_SYS_ID_MESSAGE,
    SERVICENOW_APPROVER,
)
from app.core.logging import get_logger
from app.domain.enums.approval import ApprovalStatus, ApprovalType, ServiceNowSyncStatus
from app.infrastructure.database.models.user_approval import UserApproval
from app.infrastructure.database.repositories.user_approval import (
    UserApprovalRepository,
)

logger = get_logger(__name__)


# ============================================================
# Approval Service
# ============================================================


class ApprovalService:
    """
    Handles user approval business logic.
    """

    # ============================================================
    # Constructor
    # ============================================================

    def __init__(
        self,
        db: AsyncSession,
    ) -> None:
        self._db = db

        """
        Initialize the approval service.
        """
        self._approvals = UserApprovalRepository(db)

    # ============================================================
    # Public Methods
    # ============================================================

    async def create_manual_approval(
        self,
        user_id: UUID,
    ) -> UserApproval:
        """
        Create a manual approval record.
        """

        approval = UserApproval(
            user_id=user_id,
            status=ApprovalStatus.PENDING,
            approval_type=ApprovalType.MANUAL,
            servicenow_sync_status=ServiceNowSyncStatus.PENDING,
        )

        return await self._approvals.create(
            approval,
        )

    async def create_auto_approval(
        self,
        user_id: UUID,
    ) -> UserApproval:
        """
        Automatically approve an existing
        ServiceNow user.
        """

        approval = UserApproval(
            user_id=user_id,
            status=ApprovalStatus.APPROVED,
            approval_type=ApprovalType.AUTO,
            servicenow_sync_status=ServiceNowSyncStatus.NOT_REQUIRED,
        )

        return await self._approvals.create(
            approval,
        )

    async def get_latest_approval(
        self,
        user_id: UUID,
    ) -> UserApproval | None:
        """
        Retrieve the latest approval record
        for a user.
        """

        return await self._approvals.get_latest_by_user(
            user_id,
        )

    async def can_user_login(
        self,
        user_id: UUID,
    ) -> bool:
        """
        Determine whether the user is allowed
        to access the platform.
        """

        approval = await self.get_latest_approval(
            user_id,
        )

        if approval is None:
            logger.warning(
                "No approval record found for user %s.",
                user_id,
            )
            return False

        return approval.status == ApprovalStatus.APPROVED

    async def update_servicenow_reference(
        self,
        approval: UserApproval,
        *,
        sys_id: str,
        number: str,
    ) -> UserApproval:
        """
        Store the ServiceNow record identifiers after
        successful synchronization.
        """

        approval.servicenow_sys_id = sys_id
        approval.servicenow_number = number
        approval.servicenow_sync_status = ServiceNowSyncStatus.SYNCED
        approval.servicenow_sync_error = None
        approval.retry_count = 0

        return await self._approvals.update(
            approval,
        )

    async def mark_servicenow_sync_failed(
        self,
        approval: UserApproval,
        error: str,
    ) -> UserApproval:
        """
        Mark a failed synchronization attempt.
        """

        approval.servicenow_sync_status = ServiceNowSyncStatus.FAILED
        approval.servicenow_sync_error = error
        approval.retry_count += 1

        return await self._approvals.update(
            approval,
        )

    async def mark_servicenow_retrying(
        self,
        approval: UserApproval,
    ) -> UserApproval:
        """
        Mark the approval as waiting for another
        synchronization attempt.
        """

        approval.servicenow_sync_status = ServiceNowSyncStatus.RETRYING

        return await self._approvals.update(
            approval,
        )

    async def process_callback(
        self,
        callback: ApprovalCallbackRequest,
    ) -> UserApproval:
        """
        Process an approval callback received from ServiceNow.
        """

        approval = await self._approvals.get_by_user_and_servicenow_number(
            user_id=callback.fastapi_user_id,
            approval_number=callback.approval_request_number,
        )

        approval = self._validate_callback(
            approval,
            callback,
        )

        try:
            if callback.action == "approved":
                approval = await self._process_approved_callback(
                    approval,
                )
            else:
                approval = await self._process_rejected_callback(
                    approval,
                    callback,
                )

            await self._db.commit()

            return approval

        except Exception:
            await self._db.rollback()
            raise

    def _validate_callback(
        self,
        approval: UserApproval | None,
        callback: ApprovalCallbackRequest,
    ) -> UserApproval:
        """
        Validate an approval callback received from ServiceNow.
        """

        if approval is None:
            logger.warning(
                "Approval callback received for unknown approval '%s' for user '%s'.",
                callback.approval_request_number,
                callback.fastapi_user_id,
            )
            raise ApprovalNotFoundError()

        if approval.status != ApprovalStatus.PENDING:
            logger.warning(
                "Duplicate callback received for approval '%s'. Current status: %s.",
                approval.servicenow_number,
                approval.status.value,
            )
            raise ApprovalAlreadyProcessedError()

        if callback.action == "approved" and not callback.servicenow_user_sys_id:
            raise InvalidApprovalCallbackError(
                APPROVED_CALLBACK_MISSING_USER_SYS_ID_MESSAGE,
            )

        # if callback.action == "rejected" and not callback.reason:
        #     raise InvalidApprovalCallbackError(
        #         REJECTED_CALLBACK_MISSING_REASON_MESSAGE,
        #     )

        return approval

    async def _process_approved_callback(
        self,
        approval: UserApproval,
    ) -> UserApproval:
        """
        Process an approved callback received from ServiceNow.
        """
        now = datetime.now(timezone.utc)
        approval.status = ApprovalStatus.APPROVED
        approval.approved_by = SERVICENOW_APPROVER
        approval.approved_at = now

        approval.rejected_at = None
        approval.rejection_reason = None

        return await self._approvals.update(
            approval,
        )

    async def _process_rejected_callback(
        self,
        approval: UserApproval,
        callback: ApprovalCallbackRequest,
    ) -> UserApproval:
        """
        Process a rejected callback received from ServiceNow.
        """
        now = datetime.now(timezone.utc)
        approval.status = ApprovalStatus.REJECTED
        approval.rejected_at = now
        approval.rejection_reason = callback.reason

        approval.approved_at = None
        approval.approved_by = None

        return await self._approvals.update(
            approval,
        )
