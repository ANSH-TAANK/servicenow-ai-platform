"""
Authentication Exceptions

Purpose:
- Define authentication-related exceptions.
- Represent authentication business rule failures.

This module DOES NOT:
- Generate JWT tokens.
- Hash passwords.
- Access the database.
"""

from http import HTTPStatus
from typing import Any

from app.core.constants import (
    AUTH_USER_NOT_VERIFIED,
    AUTHENTICATION_ERROR,
    EMAIL_ALREADY_EXISTS_ERROR,
    INVALID_CREDENTIALS_ERROR,
    INVALID_PASSWORD_ERROR,
    INVALID_USERNAME_ERROR,
    USER_INACTIVE_ERROR,
    USER_NOT_FOUND_ERROR,
    USERNAME_ALREADY_EXISTS_ERROR,
    VERIFICATION_ALREADY_COMPLETED_ERROR,
    VERIFICATION_ATTEMPTS_EXCEEDED_ERROR,
    VERIFICATION_CODE_EXPIRED_ERROR,
    VERIFICATION_CODE_INVALID_ERROR,
    VERIFICATION_CODE_NOT_FOUND_ERROR,
    VERIFICATION_RESEND_LIMIT_EXCEEDED_ERROR,
    VERIFICATION_RESEND_TOO_SOON_ERROR,
)
from app.exceptions.base import BaseApplicationException

# ============================================================
# Base Authentication Exception
# ============================================================


class AuthenticationError(
    BaseApplicationException,
):
    """
    Base class for all authentication exceptions.
    """

    def __init__(
        self,
        message: str,
        *,
        error_code: str = AUTHENTICATION_ERROR,
        status_code: HTTPStatus = HTTPStatus.BAD_REQUEST,
        details: Any | None = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=status_code,
            details=details,
        )


# ============================================================
# Email Already Exists
# ============================================================


class EmailAlreadyExistsError(
    AuthenticationError,
):
    """
    Raised when an email address
    already exists.
    """

    def __init__(
        self,
        message: str = ("A user with this email already exists."),
    ) -> None:
        super().__init__(
            message=message,
            error_code=EMAIL_ALREADY_EXISTS_ERROR,
            status_code=HTTPStatus.CONFLICT,
        )


# ============================================================
# Username Already Exists
# ============================================================


class UsernameAlreadyExistsError(
    AuthenticationError,
):
    """
    Raised when a username
    already exists.
    """

    def __init__(
        self,
        *,
        message: str = ("A user with this username already exists."),
        suggestions: list[str] | None = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code=USERNAME_ALREADY_EXISTS_ERROR,
            status_code=HTTPStatus.CONFLICT,
            details={
                "suggestions": suggestions or [],
            },
        )


# ============================================================
# User Not Found
# ============================================================


class UserNotFoundError(AuthenticationError):
    """
    Raised when a user cannot be found.
    """

    def __init__(
        self,
        message: str = "User not found.",
    ) -> None:
        super().__init__(
            message=message,
            error_code=USER_NOT_FOUND_ERROR,
            status_code=HTTPStatus.NOT_FOUND,
        )


# ============================================================
# Invalid Credentials
# ============================================================


class InvalidCredentialsError(AuthenticationError):
    """
    Raised when login credentials are invalid.
    """

    def __init__(
        self,
        message: str = "Invalid credentials.",
    ) -> None:
        super().__init__(
            message=message,
            error_code=INVALID_CREDENTIALS_ERROR,
            status_code=HTTPStatus.UNAUTHORIZED,
        )


# ============================================================
# Inactive User
# ============================================================


class UserInactiveError(AuthenticationError):
    """
    Raised when an inactive user
    attempts to authenticate.
    """

    def __init__(
        self,
        message: str = "User account is inactive.",
    ) -> None:
        super().__init__(
            message=message,
            error_code=USER_INACTIVE_ERROR,
            status_code=HTTPStatus.FORBIDDEN,
        )


# ============================================================
# Invalid Password
# ============================================================


class InvalidPasswordError(AuthenticationError):
    """
    Raised when a password does not satisfy
    the platform password policy.
    """

    def __init__(
        self,
        message: str = "Password does not satisfy the password policy.",
    ) -> None:
        super().__init__(
            message=message,
            error_code=INVALID_PASSWORD_ERROR,
            status_code=HTTPStatus.BAD_REQUEST,
        )


# ============================================================
# Invalid Username
# ============================================================


class InvalidUsernameError(AuthenticationError):
    """
    Raised when a username does not satisfy
    the platform username policy.
    """

    def __init__(
        self,
        message: str = "Username does not satisfy the username policy.",
    ) -> None:
        super().__init__(
            message=message,
            error_code=INVALID_USERNAME_ERROR,
            status_code=HTTPStatus.BAD_REQUEST,
        )


# ============================================================
# Verification Code Not Found
# ============================================================


class VerificationCodeNotFoundError(
    AuthenticationError,
):
    """
    Raised when a verification code
    cannot be found.
    """

    def __init__(
        self,
        message: str = "Verification code not found.",
    ) -> None:
        super().__init__(
            message=message,
            error_code=VERIFICATION_CODE_NOT_FOUND_ERROR,
            status_code=HTTPStatus.NOT_FOUND,
        )


# ============================================================
# Verification Code Expired
# ============================================================


class VerificationCodeExpiredError(
    AuthenticationError,
):
    """
    Raised when a verification code
    has expired.
    """

    def __init__(
        self,
        message: str = "Verification code has expired.",
    ) -> None:
        super().__init__(
            message=message,
            error_code=VERIFICATION_CODE_EXPIRED_ERROR,
            status_code=HTTPStatus.BAD_REQUEST,
        )


# ============================================================
# Verification Code Invalid
# ============================================================


class VerificationCodeInvalidError(
    AuthenticationError,
):
    """
    Raised when an invalid verification
    code is provided.
    """

    def __init__(
        self,
        message: str = "Invalid verification code.",
    ) -> None:
        super().__init__(
            message=message,
            error_code=VERIFICATION_CODE_INVALID_ERROR,
            status_code=HTTPStatus.BAD_REQUEST,
        )


# ============================================================
# Verification Attempts Exceeded
# ============================================================


class VerificationAttemptsExceededError(
    AuthenticationError,
):
    """
    Raised when the maximum number of
    verification attempts has been exceeded.
    """

    def __init__(
        self,
        message: str = ("Maximum verification attempts exceeded."),
    ) -> None:
        super().__init__(
            message=message,
            error_code=VERIFICATION_ATTEMPTS_EXCEEDED_ERROR,
            status_code=HTTPStatus.TOO_MANY_REQUESTS,
        )


# ============================================================
# Verification Resend Limit Exceeded
# ============================================================


class VerificationResendLimitExceededError(
    AuthenticationError,
):
    """
    Raised when the maximum number of
    verification code resend requests
    has been exceeded.
    """

    def __init__(
        self,
        message: str = ("Verification resend limit exceeded."),
    ) -> None:
        super().__init__(
            message=message,
            error_code=VERIFICATION_RESEND_LIMIT_EXCEEDED_ERROR,
            status_code=HTTPStatus.TOO_MANY_REQUESTS,
        )


# ============================================================
# Verification Resend Too Soon
# ============================================================


class VerificationResendTooSoonError(
    AuthenticationError,
):
    """
    Raised when a verification code
    is requested before the resend
    cooldown has elapsed.
    """

    def __init__(
        self,
        message: str = ("Please wait before requesting another verification code."),
    ) -> None:
        super().__init__(
            message=message,
            error_code=VERIFICATION_RESEND_TOO_SOON_ERROR,
            status_code=HTTPStatus.TOO_MANY_REQUESTS,
        )


# ============================================================
# Verification Already Completed
# ============================================================


class VerificationAlreadyCompletedError(
    AuthenticationError,
):
    """
    Raised when the user's email
    has already been verified.
    """

    def __init__(
        self,
        message: str = ("Email has already been verified."),
    ) -> None:
        super().__init__(
            message=message,
            error_code=VERIFICATION_ALREADY_COMPLETED_ERROR,
            status_code=HTTPStatus.CONFLICT,
        )


class UserNotVerifiedError(AuthenticationError):
    """
    Raised when a user attempts to authenticate
    before verifying their email address.
    """

    def __init__(
        self,
        message: str = ("Please verify your email address before logging in."),
    ) -> None:
        super().__init__(
            message=message,
            error_code=AUTH_USER_NOT_VERIFIED,
        )
