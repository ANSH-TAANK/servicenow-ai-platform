"""
Verification Code Repository

Purpose:
- Provide database access for verification codes.
- Encapsulate verification code queries.
- Reuse common CRUD operations from BaseRepository.

This module DOES NOT:
- Generate verification codes.
- Verify submitted codes.
- Send emails.
"""

import uuid
from datetime import datetime

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.verification.enums import VerificationPurpose
from app.infrastructure.database.models.verification_code import VerificationCode
from app.infrastructure.database.repositories.base import BaseRepository

# ============================================================
# Verification Code Repository
# ============================================================


class VerificationCodeRepository(
    BaseRepository[VerificationCode],
):
    """
    Repository for VerificationCode entities.
    """

    def __init__(
        self,
        db: AsyncSession,
    ) -> None:
        """
        Initialize the verification code repository.
        """

        super().__init__(
            db=db,
            model=VerificationCode,
        )

    # ============================================================
    # Get By ID
    # ============================================================

    async def get_by_id(
        self,
        verification_code_id: uuid.UUID,
    ) -> VerificationCode | None:
        """
        Retrieve a verification code by its ID.
        """

        statement = select(
            VerificationCode,
        ).where(
            VerificationCode.id == verification_code_id,
        )

        result = await self._db.execute(statement)

        return result.scalar_one_or_none()

    # ============================================================
    # Get Latest By User And Purpose
    # ============================================================

    async def get_latest_by_user_and_purpose(
        self,
        user_id: uuid.UUID,
        purpose: VerificationPurpose,
    ) -> VerificationCode | None:
        """
        Retrieve the most recently created verification code
        for a user and purpose.
        """

        statement = (
            select(VerificationCode)
            .where(
                VerificationCode.user_id == user_id,
                VerificationCode.purpose == purpose,
            )
            .order_by(
                VerificationCode.created_at.desc(),
            )
            .limit(1)
        )

        result = await self._db.execute(statement)

        return result.scalar_one_or_none()

    # ============================================================
    # Delete Expired
    # ============================================================

    async def delete_expired(
        self,
        current_time: datetime,
    ) -> None:
        """
        Delete all expired verification codes.
        """

        statement = delete(
            VerificationCode,
        ).where(
            VerificationCode.expires_at < current_time,
        )

        await self._db.execute(statement)

        await self._db.flush()

    # ============================================================
    # Delete By User
    # ============================================================

    async def delete_by_user(
        self,
        user_id: uuid.UUID,
    ) -> None:
        """
        Delete all verification codes belonging to a user.
        """

        statement = delete(
            VerificationCode,
        ).where(
            VerificationCode.user_id == user_id,
        )

        await self._db.execute(statement)

        await self._db.flush()
