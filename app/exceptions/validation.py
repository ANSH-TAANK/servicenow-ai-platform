"""
Validation Exceptions

Purpose:
- Define validation related exceptions.
"""

from app.exceptions.base import BaseApplicationException

# ============================================================
# Base Validation Exception
# ============================================================


class ValidationError(BaseApplicationException):
    """
    Base exception for validation errors.
    """

    def __init__(
        self,
        message: str = "Validation failed.",
        *,
        error_code: str = "VALIDATION_ERROR",
        status_code: int = 400,
    ) -> None:
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=status_code,
        )


# ============================================================
# Request Validation Exception
# ============================================================


class RequestValidationError(ValidationError):
    """
    Raised when an incoming request is invalid.
    """

    def __init__(
        self,
        message: str = "Request validation failed.",
    ) -> None:
        super().__init__(
            message=message,
            error_code="REQUEST_VALIDATION_ERROR",
            status_code=400,
        )


# ============================================================
# Business Validation Exception
# ============================================================


class BusinessValidationError(ValidationError):
    """
    Raised when business rules are violated.
    """

    def __init__(
        self,
        message: str = "Business validation failed.",
    ) -> None:
        super().__init__(
            message=message,
            error_code="BUSINESS_VALIDATION_ERROR",
            status_code=422,
        )
