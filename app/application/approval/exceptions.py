"""
Approval Exceptions

Purpose:
- Define approval-related exceptions.
- Represent approval business rule failures.
"""

from http import HTTPStatus

from app.core.constants import USER_APPROVAL_PENDING_ERROR
from app.exceptions.base import BaseApplicationException

# ============================================================
# Base Approval Exception
# ============================================================


class ApprovalError(BaseApplicationException):
    """
    Base class for all approval exceptions.
    """

    def __init__(
        self,
        message: str,
        *,
        error_code: str,
        status_code: HTTPStatus = HTTPStatus.FORBIDDEN,
    ) -> None:
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=status_code,
        )


# ============================================================
# User Approval Pending
# ============================================================


class UserApprovalPendingError(
    ApprovalError,
):
    """
    Raised when a verified user has not yet
    been approved.
    """

    def __init__(
        self,
        message: str = ("Your account is awaiting administrator approval."),
    ) -> None:
        super().__init__(
            message=message,
            error_code=USER_APPROVAL_PENDING_ERROR,
        )
