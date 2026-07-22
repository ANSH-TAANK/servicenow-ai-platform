"""
Verification Code Database Model

Purpose:
- Store verification codes for user authentication workflows.
- Support email verification and password reset.
- Track verification attempts and resend activity.

This module DOES NOT:
- Generate verification codes.
- Verify submitted codes.
- Send emails.
"""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.constants import (
    OTP_HASH_MAX_LENGTH,
    TABLE_USERS,
    TABLE_VERIFICATION_CODES,
    VERIFICATION_PURPOSE_MAX_LENGTH,
)
from app.domain.verification.enums import VerificationPurpose, VerificationStatus
from app.infrastructure.database.base import Base
from app.infrastructure.database.mixins import TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.infrastructure.database.models.user import User


# ============================================================
# Verification Code Model
# ============================================================


class VerificationCode(
    UUIDMixin,
    TimestampMixin,
    Base,
):
    """
    Represents a verification code issued to a user.
    """

    __tablename__ = TABLE_VERIFICATION_CODES

    # ============================================================
    # Ownership
    # ============================================================

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(f"{TABLE_USERS}.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ============================================================
    # Verification Details
    # ============================================================

    purpose: Mapped[VerificationPurpose] = mapped_column(
        Enum(
            VerificationPurpose,
            native_enum=False,
            validate_strings=True,
            length=VERIFICATION_PURPOSE_MAX_LENGTH,
        ),
        nullable=False,
    )

    status: Mapped[VerificationStatus] = mapped_column(
        Enum(
            VerificationStatus,
            native_enum=False,
            validate_strings=True,
        ),
        default=VerificationStatus.PENDING,
        nullable=False,
    )

    code_hash: Mapped[str] = mapped_column(
        String(OTP_HASH_MAX_LENGTH),
        nullable=False,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # ============================================================
    # Security
    # ============================================================

    failed_attempts: Mapped[int] = mapped_column(
        Integer,
        default=0,
        server_default="0",
        nullable=False,
    )

    resend_attempts: Mapped[int] = mapped_column(
        Integer,
        default=0,
        server_default="0",
        nullable=False,
    )

    last_resend_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # ============================================================
    # Relationships
    # ============================================================

    user: Mapped["User"] = relationship(
        back_populates="verification_codes",
    )
