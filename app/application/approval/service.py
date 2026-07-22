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

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.domain.enums.approval import ApprovalStatus, ApprovalType
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
        """
        Initialize the approval service.
        """

        self._db = db
        self._approvals = UserApprovalRepository(db)

    # ============================================================
    # Public Methods
    # ============================================================

    async def create_initial_approval(
        self,
        user_id: UUID,
    ) -> None:
        """
        Create the initial approval record for a newly
        verified user.
        """

        approval = UserApproval(
            user_id=user_id,
            status=ApprovalStatus.PENDING,
            approval_type=ApprovalType.MANUAL,
        )

        await self._approvals.create(
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
