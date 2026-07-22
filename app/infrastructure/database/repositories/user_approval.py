"""
User Approval Repository

Purpose:
- Provide database access for user approval records.
- Encapsulate approval queries.
- Reuse common CRUD operations from BaseRepository.

This module DOES NOT:
- Approve users.
- Reject users.
- Contain business logic.
"""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.enums.approval import ApprovalStatus
from app.infrastructure.database.models.user_approval import UserApproval
from app.infrastructure.database.repositories.base import BaseRepository

# ============================================================
# User Approval Repository
# ============================================================


class UserApprovalRepository(
    BaseRepository[UserApproval],
):
    """
    Repository for UserApproval entities.
    """

    def __init__(
        self,
        db: AsyncSession,
    ) -> None:
        """
        Initialize the user approval repository.
        """

        super().__init__(
            db=db,
            model=UserApproval,
        )

    # ============================================================
    # Get By ID
    # ============================================================

    async def get_by_id(
        self,
        approval_id: uuid.UUID,
    ) -> UserApproval | None:
        """
        Retrieve an approval record by its ID.
        """

        statement = select(
            UserApproval,
        ).where(
            UserApproval.id == approval_id,
        )

        result = await self._db.execute(statement)

        return result.scalar_one_or_none()

    # ============================================================
    # Get Latest By User
    # ============================================================

    async def get_latest_by_user(
        self,
        user_id: uuid.UUID,
    ) -> UserApproval | None:
        """
        Retrieve the latest approval record for a user.
        """

        statement = (
            select(UserApproval)
            .where(
                UserApproval.user_id == user_id,
            )
            .order_by(
                UserApproval.created_at.desc(),
            )
            .limit(1)
        )

        result = await self._db.execute(statement)

        return result.scalar_one_or_none()

    # ============================================================
    # Get By Status
    # ============================================================

    async def get_by_status(
        self,
        status: ApprovalStatus,
    ) -> list[UserApproval]:
        """
        Retrieve all approval records with the given status.
        """

        statement = select(
            UserApproval,
        ).where(
            UserApproval.status == status,
        )

        result = await self._db.execute(statement)

        return list(result.scalars().all())
