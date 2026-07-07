"""
Testing Database

Purpose:
- Provide database helpers for tests.
- Create testing sessions.
- Isolate testing infrastructure from application code.
"""

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.infrastructure.database.engine import engine

# ============================================================
# Test Session Factory
# ============================================================

TestSessionFactory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False,
)
