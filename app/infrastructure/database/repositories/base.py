"""
Base Repository

Purpose:
- Provide reusable CRUD operations.
- Serve as the parent repository for all entities.
- Encapsulate common database access logic.

This module DOES NOT:
- Contain business logic.
- Know about specific entities.
- Call external services.
"""

from typing import Any, Generic, TypeVar

from sqlalchemy import exists, func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.base import Base

# ============================================================
# Generic Type
# ============================================================

T = TypeVar("T", bound=Base)

# ============================================================
# Base Repository
# ============================================================


class BaseRepository(Generic[T]):
    """
    Generic repository providing reusable CRUD operations.

    This class should be inherited by all entity-specific
    repositories.
    """

    def __init__(
        self,
        db: AsyncSession,
        model: type[T],
    ) -> None:
        """
        Initialize the repository.

        Args:
            db:
                Active SQLAlchemy async session.

            model:
                ORM model managed by this repository.
        """

        self._db = db
        self._model = model

    # ============================================================
    # Create
    # ============================================================

    async def create(
        self,
        entity: T,
    ) -> T:
        """
        Stage a new entity for persistence.

        The entity is flushed to the database so generated
        values (e.g. primary keys) are available immediately,
        but the transaction is NOT committed.

        The caller is responsible for committing.
        """

        try:
            self._db.add(entity)

            await self._db.flush()

            await self._db.refresh(entity)

            return entity

        except SQLAlchemyError:
            await self._db.rollback()
            raise

    # ============================================================
    # Get All
    # ============================================================

    async def get_all(
        self,
        *conditions: Any,
    ) -> list[T]:
        """
        Retrieve all entities matching the given conditions.

        Args:
            *conditions:
                SQLAlchemy filter expressions.

        Returns:
            List of matching entities.
        """

        statement = select(self._model)

        if conditions:
            statement = statement.where(*conditions)

        result = await self._db.execute(statement)

        return list(result.scalars().all())

    # ============================================================
    # Count
    # ============================================================

    async def count(self) -> int:
        """
        Count all entities.

        Returns:
            Total number of entities.
        """

        statement = select(func.count()).select_from(self._model)

        result = await self._db.execute(statement)

        return result.scalar_one()

    # ============================================================
    # Exists
    # ============================================================

    async def exists(
        self,
        *conditions: Any,
    ) -> bool:
        """
        Determine whether any entity matches the given conditions.

        Args:
            *conditions:
                SQLAlchemy filter expressions.

        Returns:
            True if at least one matching entity exists,
            otherwise False.
        """

        statement = select(exists(select(self._model).where(*conditions)))

        result = await self._db.execute(statement)

        return result.scalar_one()

    # ============================================================
    # Update
    # ============================================================

    async def update(
        self,
        entity: T,
    ) -> T:
        """
        Flush changes made to an existing entity.

        The transaction is NOT committed.
        The caller is responsible for committing.
        """

        try:
            await self._db.flush()

            await self._db.refresh(entity)

            return entity

        except SQLAlchemyError:
            await self._db.rollback()
            raise

    # ============================================================
    # Hard Delete
    # ============================================================

    async def hard_delete(
        self,
        entity: T,
    ) -> None:
        """
        Stage an entity for permanent deletion.

        The deletion is flushed to the database but
        the transaction is NOT committed.

        The caller is responsible for committing.
        """

        try:
            await self._db.delete(entity)

            await self._db.flush()

        except SQLAlchemyError:
            await self._db.rollback()
            raise
