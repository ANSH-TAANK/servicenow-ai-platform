"""
ServiceNow Connection Database Model

Purpose:
- Store ServiceNow connection information.
- Maintain the authenticated connection between a user and a ServiceNow instance.

This module DOES NOT:
- Authenticate users.
- Call ServiceNow APIs.
- Contain business logic.
"""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.constants import (
    ENCRYPTED_CREDENTIAL_MAX_LENGTH,
    INSTANCE_NAME_MAX_LENGTH,
    INSTANCE_URL_MAX_LENGTH,
    SERVICENOW_USERNAME_MAX_LENGTH,
    TABLE_SERVICENOW_CONNECTIONS,
    TABLE_USERS,
)
from app.domain.enums.connection import ConnectionStatus
from app.infrastructure.database.base import Base
from app.infrastructure.database.mixins import (
    ActiveMixin,
    SoftDeleteMixin,
    TimestampMixin,
    UUIDMixin,
)

if TYPE_CHECKING:
    from app.infrastructure.database.models.user import User

# ============================================================
# ServiceNow Connection Model
# ============================================================


class ServiceNowConnection(
    UUIDMixin,
    TimestampMixin,
    SoftDeleteMixin,
    ActiveMixin,
    Base,
):
    """
    Represents a ServiceNow connection for a platform user.
    """

    __tablename__ = TABLE_SERVICENOW_CONNECTIONS

    # ============================================================
    # User Relationship
    # ============================================================

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            f"{TABLE_USERS}.id",
            ondelete="CASCADE",
        ),
        unique=True,
        nullable=False,
    )

    # ============================================================
    # Instance Information
    # ============================================================

    instance_url: Mapped[str] = mapped_column(
        String(INSTANCE_URL_MAX_LENGTH),
        nullable=False,
        index=True,
    )

    instance_name: Mapped[str] = mapped_column(
        String(INSTANCE_NAME_MAX_LENGTH),
        nullable=False,
    )

    username: Mapped[str] = mapped_column(
        String(SERVICENOW_USERNAME_MAX_LENGTH),
        nullable=False,
    )

    # ============================================================
    # Credentials
    # ============================================================

    credential_ciphertext: Mapped[str] = mapped_column(
        String(ENCRYPTED_CREDENTIAL_MAX_LENGTH),
        nullable=False,
    )

    credential_version: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )

    # ============================================================
    # Connection Status
    # ============================================================

    status: Mapped[ConnectionStatus] = mapped_column(
        Enum(
            ConnectionStatus,
            native_enum=False,
            validate_strings=True,
        ),
        default=ConnectionStatus.ACTIVE,
        nullable=False,
        index=True,
    )

    # ============================================================
    # Activity
    # ============================================================

    last_connected_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    last_verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # ============================================================
    # Relationships
    # ============================================================

    user: Mapped["User"] = relationship(
        back_populates="servicenow_connection",
    )
