"""
User Repository

Purpose:
- Provide database operations specific to the User entity.
- Extend the generic BaseRepository.
- Encapsulate User-specific queries.

This module DOES NOT:
- Contain business logic.
- Authenticate users.
- Call external APIs.
"""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models.user import User
from app.infrastructure.database.repositories.base import BaseRepository

# ============================================================
# User Repository
# ============================================================


class UserRepository(BaseRepository[User]):
    """
    Repository for User database operations.

    Extends the generic BaseRepository with
    User-specific query methods.
    """

    # ============================================================
    # Constructor
    # ============================================================

    def __init__(
        self,
        db: AsyncSession,
    ) -> None:
        """
        Initialize the User repository.

        Args:
            db:
                Active SQLAlchemy async session.
        """

        super().__init__(
            db=db,
            model=User,
        )

    # ============================================================
    # Get By ID
    # ============================================================

    async def get_by_id(
        self,
        user_id: uuid.UUID,
    ) -> User | None:
        """
        Retrieve a user by its unique identifier.

        Args:
            user_id:
                UUID of the user.

        Returns:
            User if found, otherwise None.
        """

        statement = select(User).where(
            User.id == user_id,
        )

        result = await self._db.execute(statement)

        return result.scalar_one_or_none()

    # ============================================================
    # Get By Email
    # ============================================================

    async def get_by_email(
        self,
        email: str,
    ) -> User | None:
        """
        Retrieve a user by email address.

        Args:
            email:
                User email address.

        Returns:
            User if found, otherwise None.
        """

        statement = select(User).where(
            User.email == email,
        )

        result = await self._db.execute(statement)

        return result.scalar_one_or_none()

    # ============================================================
    # Get By Username
    # ============================================================

    async def get_by_username(
        self,
        username: str,
    ) -> User | None:
        """
        Retrieve a user by username.

        Args:
            username:
                User's username.

        Returns:
            User if found, otherwise None.
        """

        statement = select(User).where(
            User.username == username,
        )

        result = await self._db.execute(statement)

        return result.scalar_one_or_none()

    # ============================================================
    # Get By ServiceNow sys_id
    # ============================================================

    async def get_by_servicenow_sys_id(
        self,
        servicenow_sys_id: str,
    ) -> User | None:
        """
        Retrieve a user by ServiceNow sys_id.

        Args:
            servicenow_sys_id:
                ServiceNow user sys_id.

        Returns:
            User if found, otherwise None.
        """

        statement = select(User).where(
            User.servicenow_sys_id == servicenow_sys_id,
        )

        result = await self._db.execute(statement)

        return result.scalar_one_or_none()
