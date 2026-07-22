"""
User Approval Database Model

Purpose:
- Store user approval records.
- Track the approval lifecycle of a user.
- Preserve approval history.

This module DOES NOT:
- Approve users.
- Reject users.
- Contain business logic.
"""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.constants import (
    APPROVAL_REASON_MAX_LENGTH,
    APPROVED_BY_MAX_LENGTH,
    TABLE_USER_APPROVALS,
    TABLE_USERS,
)
from app.domain.enums.approval import ApprovalStatus, ApprovalType
from app.infrastructure.database.base import Base
from app.infrastructure.database.mixins import TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.infrastructure.database.models.user import User


# ============================================================
# User Approval Model
# ============================================================


class UserApproval(
    UUIDMixin,
    TimestampMixin,
    Base,
):
    """
    Represents an approval record for a user.
    """

    __tablename__ = TABLE_USER_APPROVALS

    # ============================================================
    # User Relationship
    # ============================================================

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            f"{TABLE_USERS}.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    # ============================================================
    # Approval
    # ============================================================

    status: Mapped[ApprovalStatus] = mapped_column(
        Enum(
            ApprovalStatus,
            native_enum=False,
            validate_strings=True,
        ),
        default=ApprovalStatus.PENDING,
        nullable=False,
        index=True,
    )

    approval_type: Mapped[ApprovalType] = mapped_column(
        Enum(
            ApprovalType,
            native_enum=False,
            validate_strings=True,
        ),
        default=ApprovalType.MANUAL,
        nullable=False,
    )

    # ============================================================
    # Approval Details
    # ============================================================

    approved_by: Mapped[str | None] = mapped_column(
        String(APPROVED_BY_MAX_LENGTH),
        nullable=True,
    )

    approved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    rejected_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    rejection_reason: Mapped[str | None] = mapped_column(
        String(APPROVAL_REASON_MAX_LENGTH),
        nullable=True,
    )

    # ============================================================
    # Relationships
    # ============================================================

    user: Mapped["User"] = relationship(
        back_populates="approvals",
    )
