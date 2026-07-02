"""
Database Engine

Purpose:
- Create the SQLAlchemy async engine.
- Build the database connection URL.
- Configure connection pooling.

This module DOES NOT:
- Create sessions
- Create tables
- Execute queries
"""

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.core.config import settings

# ============================================================
# Database URL Builder
# ============================================================


def build_database_url() -> str:
    """
    Build the PostgreSQL connection URL
    from application settings.
    """

    return (
        f"postgresql+asyncpg://"
        f"{settings.database.username}:"
        f"{settings.database.password}@"
        f"{settings.database.host}:"
        f"{settings.database.port}/"
        f"{settings.database.name}"
    )


# ============================================================
# Database Engine
# ============================================================

engine: AsyncEngine = create_async_engine(
    build_database_url(),
    echo=settings.database.echo,
    pool_pre_ping=True,
    pool_size=settings.database.pool_size,
    max_overflow=settings.database.max_overflow,
    pool_timeout=settings.database.pool_timeout,
    pool_recycle=settings.database.pool_recycle,
)
