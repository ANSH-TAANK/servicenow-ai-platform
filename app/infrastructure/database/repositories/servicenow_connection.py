"""
ServiceNow Connection Repository

Purpose:
- Provide database operations specific to the ServiceNowConnection entity.
- Extend the generic BaseRepository.
- Encapsulate ServiceNow connection-specific queries.

This module DOES NOT:
- Contain business logic.
- Authenticate ServiceNow instances.
- Call ServiceNow APIs.
"""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.enums.connection import ConnectionStatus
from app.infrastructure.database.models.servicenow_connection import (
    ServiceNowConnection,
)
from app.infrastructure.database.repositories.base import BaseRepository

# ============================================================
# ServiceNow Connection Repository
# ============================================================


class ServiceNowConnectionRepository(
    BaseRepository[ServiceNowConnection],
):
    """
    Repository for ServiceNowConnection database operations.
    """

    # ============================================================
    # Constructor
    # ============================================================

    def __init__(
        self,
        db: AsyncSession,
    ) -> None:
        """
        Initialize the ServiceNowConnection repository.

        Args:
            db:
                Active SQLAlchemy async session.
        """

        super().__init__(
            db=db,
            model=ServiceNowConnection,
        )

    # ============================================================
    # Get By ID
    # ============================================================

    async def get_by_id(
        self,
        connection_id: uuid.UUID,
    ) -> ServiceNowConnection | None:
        """
        Retrieve a ServiceNow connection by its unique identifier.
        """

        statement = select(
            ServiceNowConnection,
        ).where(
            ServiceNowConnection.id == connection_id,
        )

        result = await self._db.execute(statement)

        return result.scalar_one_or_none()

    # ============================================================
    # Get By User ID
    # ============================================================

    async def get_by_user_id(
        self,
        user_id: uuid.UUID,
    ) -> ServiceNowConnection | None:
        """
        Retrieve the ServiceNow connection for a user.
        """

        statement = select(
            ServiceNowConnection,
        ).where(
            ServiceNowConnection.user_id == user_id,
        )

        result = await self._db.execute(statement)

        return result.scalar_one_or_none()

    # ============================================================
    # Get By Instance URL
    # ============================================================

    async def get_by_instance_url(
        self,
        instance_url: str,
    ) -> ServiceNowConnection | None:
        """
        Retrieve a ServiceNow connection by instance URL.
        """

        statement = select(
            ServiceNowConnection,
        ).where(
            ServiceNowConnection.instance_url == instance_url,
        )

        result = await self._db.execute(statement)

        return result.scalar_one_or_none()

    # ============================================================
    # Get Active Connection
    # ============================================================

    async def get_active_connection(
        self,
        user_id: uuid.UUID,
    ) -> ServiceNowConnection | None:
        """
        Retrieve the active ServiceNow connection for a user.
        """

        statement = select(
            ServiceNowConnection,
        ).where(
            ServiceNowConnection.user_id == user_id,
            ServiceNowConnection.status == ConnectionStatus.ACTIVE,
            ServiceNowConnection.is_active.is_(True),
            ServiceNowConnection.deleted_at.is_(None),
        )

        result = await self._db.execute(statement)

        return result.scalar_one_or_none()
