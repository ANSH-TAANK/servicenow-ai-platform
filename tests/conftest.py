"""
Pytest Fixtures

Purpose:
- Provide reusable fixtures for repository and integration tests.
- Manage database session lifecycle.
- Ensure database isolation between tests.
"""

from collections.abc import AsyncGenerator

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import SessionFactory

# ============================================================
# Database Session Fixture
# ============================================================


@pytest_asyncio.fixture
async def db() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide an asynchronous database session for tests.

    The session is automatically closed after each test.
    """

    async with SessionFactory() as session:
        yield session
