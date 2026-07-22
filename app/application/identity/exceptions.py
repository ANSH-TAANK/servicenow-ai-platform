"""
Identity Exceptions

Purpose:
- Define identity management exceptions.
- Represent ServiceNow identity lifecycle failures.
- Encapsulate business rule violations related to
  identity synchronization and provisioning.

This module DOES NOT:
- Call ServiceNow APIs.
- Access the database.
- Perform synchronization.
"""

from http import HTTPStatus

from app.exceptions.base import BaseApplicationException

# ============================================================
# Base Identity Exception
# ============================================================


class IdentityError(BaseApplicationException):
    """
    Base class for all identity-related exceptions.
    """

    def __init__(
        self,
        message: str,
        *,
        error_code: str = "IDENTITY_ERROR",
        status_code: int = HTTPStatus.BAD_REQUEST,
    ) -> None:
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=status_code,
        )


# ============================================================
# ServiceNow User Not Found
# ============================================================


class ServiceNowUserNotFoundError(IdentityError):
    """
    Raised when the user does not exist
    in the connected ServiceNow instance.
    """


# ============================================================
# Identity Already Linked
# ============================================================


class IdentityAlreadyLinkedError(IdentityError):
    """
    Raised when a platform user is already
    linked with a ServiceNow identity.
    """


# ============================================================
# Identity Synchronization Failed
# ============================================================


class IdentitySynchronizationError(IdentityError):
    """
    Raised when identity synchronization
    with ServiceNow fails.
    """


# ============================================================
# Identity Provisioning Failed
# ============================================================


class IdentityProvisioningError(IdentityError):
    """
    Raised when provisioning a new
    ServiceNow user fails.
    """


# ============================================================
# Identity Approval Pending
# ============================================================


class IdentityApprovalPendingError(IdentityError):
    """
    Raised when a user's provisioning request
    is awaiting administrator approval.
    """


# ============================================================
# Identity Provisioning Rejected
# ============================================================


class IdentityProvisioningRejectedError(IdentityError):
    """
    Raised when a provisioning request
    has been rejected.
    """


"""
Identity Exceptions

Purpose:
- Define application exceptions for
  identity management workflows.
"""


class PlatformUserNotFoundError(Exception):
    """
    Raised when the requested platform
    user does not exist.
    """
