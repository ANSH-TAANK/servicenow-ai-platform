"""
Database Mixins

Purpose:
- Provide reusable ORM fields.
- Avoid code duplication across models.

This module DOES NOT:
- Create tables
- Execute queries
- Create sessions
"""

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

# ============================================================
# UUID Mixin
# ============================================================


class UUIDMixin:
    """
    Provides a UUID primary key.
    """

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )


# ============================================================
# Timestamp Mixin
# ============================================================


class TimestampMixin:
    """
    Provides timestamp fields for auditing.
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


# ============================================================
# Soft Delete Mixin
# ============================================================


class SoftDeleteMixin:
    """
    Provides soft delete functionality.
    """

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


# ============================================================
# Active Mixin
# ============================================================


class ActiveMixin:
    """
    Provides an active status field.
    """

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
