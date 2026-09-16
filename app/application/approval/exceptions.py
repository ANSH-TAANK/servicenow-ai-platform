"""
Approval Exceptions

Purpose:
- Define approval-related exceptions.
- Represent approval business rule failures.
"""

from http import HTTPStatus

from app.core.constants import (
    APPROVAL_ALREADY_PROCESSED_ERROR,
    APPROVAL_ALREADY_PROCESSED_MESSAGE,
    APPROVAL_NOT_FOUND_ERROR,
    APPROVAL_NOT_FOUND_MESSAGE,
    INVALID_APPROVAL_CALLBACK_ERROR,
    USER_APPROVAL_PENDING_ERROR,
)
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


# ============================================================
# Approval Not Found
# ============================================================


class ApprovalNotFoundError(
    ApprovalError,
):
    """
    Raised when an approval record cannot be found.
    """

    def __init__(
        self,
        message: str = APPROVAL_NOT_FOUND_MESSAGE,
    ) -> None:
        super().__init__(
            message=message,
            error_code=APPROVAL_NOT_FOUND_ERROR,
            status_code=HTTPStatus.NOT_FOUND,
        )


# ============================================================
# Approval Already Processed
# ============================================================


class ApprovalAlreadyProcessedError(
    ApprovalError,
):
    """
    Raised when an approval callback is received
    for an approval that has already been processed.
    """

    def __init__(
        self,
        message: str = APPROVAL_ALREADY_PROCESSED_MESSAGE,
    ) -> None:
        super().__init__(
            message=message,
            error_code=APPROVAL_ALREADY_PROCESSED_ERROR,
            status_code=HTTPStatus.CONFLICT,
        )


# ============================================================
# Invalid Approval Callback
# ============================================================


class InvalidApprovalCallbackError(
    ApprovalError,
):
    """
    Raised when an approval callback payload
    is invalid.
    """

    def __init__(
        self,
        message: str,
    ) -> None:
        super().__init__(
            message=message,
            error_code=INVALID_APPROVAL_CALLBACK_ERROR,
            status_code=HTTPStatus.BAD_REQUEST,
        )
