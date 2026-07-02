"""
User Database Model

Purpose:
- Represent a platform user.
- Store ServiceNow user mapping.
- Serve as the parent entity for user-related data.

This module DOES NOT:
- Authenticate users.
- Call ServiceNow APIs.
- Contain business logic.
"""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.constants import (
    EMAIL_MAX_LENGTH,
    NAME_MAX_LENGTH,
    SERVICENOW_SYS_ID_LENGTH,
    TABLE_USERS,
    USERNAME_MAX_LENGTH,
)
from app.infrastructure.database.base import Base
from app.infrastructure.database.mixins import (
    ActiveMixin,
    SoftDeleteMixin,
    TimestampMixin,
    UUIDMixin,
)

if TYPE_CHECKING:
    from app.infrastructure.database.models.servicenow_connection import (
        ServiceNowConnection,
    )


# ============================================================
# User Model
# ============================================================


class User(
    UUIDMixin,
    TimestampMixin,
    SoftDeleteMixin,
    ActiveMixin,
    Base,
):
    """
    Represents a platform user.
    """

    __tablename__ = TABLE_USERS

    # ============================================================
    # ServiceNow Mapping
    # ============================================================

    servicenow_sys_id: Mapped[str | None] = mapped_column(
        String(SERVICENOW_SYS_ID_LENGTH),
        unique=True,
        nullable=True,
        index=True,
    )

    # ============================================================
    # Identity
    # ============================================================

    username: Mapped[str] = mapped_column(
        String(USERNAME_MAX_LENGTH),
        unique=True,
        nullable=False,
        index=True,
    )

    full_name: Mapped[str] = mapped_column(
        String(NAME_MAX_LENGTH),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(EMAIL_MAX_LENGTH),
        unique=True,
        nullable=False,
        index=True,
    )

    # ============================================================
    # ServiceNow Status
    # ============================================================

    is_servicenow_user: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # ============================================================
    # Activity
    # ============================================================

    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    last_synced_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # ============================================================
    # Relationships
    # ============================================================

    servicenow_connection: Mapped["ServiceNowConnection"] = relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
