"""
Database Session

Purpose:
- Create the SQLAlchemy async session factory.
- Provide database sessions.
- Manage session lifecycle.

This module DOES NOT:
- Create tables
- Execute queries
- Contain business logic
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.infrastructure.database.engine import engine

# ============================================================
# Session Factory
# ============================================================

SessionFactory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False,
)

# ============================================================
# Database Session Dependency
# ============================================================


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide a database session for each request.

    The session is automatically closed after use.
    """

    async with SessionFactory() as session:
        yield session
