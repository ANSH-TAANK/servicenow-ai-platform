"""
Database Base

Purpose:
- Define the application's Declarative Base.
- Provide the base class for all ORM models.

This module DOES NOT:
- Create tables
- Create sessions
- Execute queries
"""

from sqlalchemy.orm import DeclarativeBase

# ============================================================
# Declarative Base
# ============================================================


class Base(DeclarativeBase):
    """
    Base class for all database models.
    """

    pass
