"""
ServiceNow Exceptions

Purpose:
- Define all ServiceNow related exceptions.
"""

from app.exceptions.base import BaseApplicationException

# ============================================================
# Base ServiceNow Exception
# ============================================================


class ServiceNowError(BaseApplicationException):
    """
    Base exception for all ServiceNow errors.
    """

    def __init__(
        self,
        message: str = "ServiceNow operation failed.",
        *,
        error_code: str = "SERVICENOW_ERROR",
        status_code: int = 500,
    ) -> None:
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=status_code,
        )


# ============================================================
# Authentication Exception
# ============================================================


class ServiceNowAuthenticationError(ServiceNowError):
    """
    Raised when ServiceNow authentication fails.
    """

    def __init__(
        self,
        message: str = "ServiceNow authentication failed.",
    ) -> None:
        super().__init__(
            message=message,
            error_code="SERVICENOW_AUTHENTICATION_ERROR",
            status_code=401,
        )


# ============================================================
# API Exception
# ============================================================


class ServiceNowAPIError(ServiceNowError):
    """
    Raised when ServiceNow API request fails.
    """

    def __init__(
        self,
        message: str = "ServiceNow API request failed.",
    ) -> None:
        super().__init__(
            message=message,
            error_code="SERVICENOW_API_ERROR",
            status_code=502,
        )


# ============================================================
# Mapping Exception
# ============================================================


class ServiceNowMappingError(ServiceNowError):
    """
    Raised when payload mapping fails.
    """

    def __init__(
        self,
        message: str = "ServiceNow payload mapping failed.",
    ) -> None:
        super().__init__(
            message=message,
            error_code="SERVICENOW_MAPPING_ERROR",
            status_code=500,
        )
