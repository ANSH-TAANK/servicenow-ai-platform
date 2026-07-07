"""
Base Application Exception

Purpose:
- Define the base exception used throughout the application.
- Provide a consistent structure for all custom exceptions.
"""

from typing import Any

from app.core.constants import APPLICATION_ERROR

# ============================================================
# Base Application Exception
# ============================================================


class BaseApplicationException(Exception):
    """
    Base exception for the entire application.

    Every custom exception should inherit from this class.
    """

    def __init__(
        self,
        message: str,
        *,
        error_code: str = APPLICATION_ERROR,
        status_code: int = 500,
        details: Any | None = None,
    ) -> None:
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details

        super().__init__(message)

    def __str__(self) -> str:
        return self.message
