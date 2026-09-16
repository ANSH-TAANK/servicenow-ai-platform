"""
User Approval Database Model

Purpose:
- Store user approval records.
- Track the approval lifecycle of a user.
- Preserve approval history.
- Track synchronization with ServiceNow.

This module DOES NOT:
- Approve users.
- Reject users.
- Contain business logic.
"""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.constants import (
    APPROVAL_REASON_MAX_LENGTH,
    APPROVED_BY_MAX_LENGTH,
    SERVICENOW_NUMBER_MAX_LENGTH,
    SERVICENOW_SYNC_ERROR_MAX_LENGTH,
    SERVICENOW_SYS_ID_LENGTH,
    TABLE_USER_APPROVALS,
    TABLE_USERS,
)
from app.domain.enums.approval import ApprovalStatus, ApprovalType, ServiceNowSyncStatus
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
    # Business Approval
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
    # ServiceNow Synchronization
    # ============================================================

    servicenow_sync_status: Mapped[ServiceNowSyncStatus] = mapped_column(
        Enum(
            ServiceNowSyncStatus,
            native_enum=False,
            validate_strings=True,
        ),
        default=ServiceNowSyncStatus.PENDING,
        nullable=False,
        index=True,
    )

    servicenow_sys_id: Mapped[str | None] = mapped_column(
        String(SERVICENOW_SYS_ID_LENGTH),
        nullable=True,
        unique=True,
    )

    servicenow_number: Mapped[str | None] = mapped_column(
        String(SERVICENOW_NUMBER_MAX_LENGTH),
        nullable=True,
    )

    servicenow_sync_error: Mapped[str | None] = mapped_column(
        String(SERVICENOW_SYNC_ERROR_MAX_LENGTH),
        nullable=True,
    )

    retry_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    # ============================================================
    # Relationships
    # ============================================================

    user: Mapped["User"] = relationship(
        back_populates="approvals",
    )
