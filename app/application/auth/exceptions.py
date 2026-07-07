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

from app.core.constants import (
    AUTHENTICATION_ERROR,
    INVALID_CREDENTIALS_ERROR,
    INVALID_PASSWORD_ERROR,
    INVALID_USERNAME_ERROR,
    USER_ALREADY_EXISTS_ERROR,
    USER_INACTIVE_ERROR,
    USER_NOT_FOUND_ERROR,
)
from app.exceptions.base import BaseApplicationException

# ============================================================
# Base Authentication Exception
# ============================================================


class AuthenticationError(BaseApplicationException):
    """
    Base class for all authentication exceptions.
    """

    def __init__(
        self,
        message: str,
        *,
        error_code: str = AUTHENTICATION_ERROR,
        status_code: HTTPStatus = HTTPStatus.BAD_REQUEST,
    ) -> None:
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=status_code,
        )


# ============================================================
# User Already Exists
# ============================================================


class UserAlreadyExistsError(AuthenticationError):
    """
    Raised when attempting to register
    an existing user.
    """

    def __init__(
        self,
        message: str = "User already exists.",
    ) -> None:
        super().__init__(
            message=message,
            error_code=USER_ALREADY_EXISTS_ERROR,
            status_code=HTTPStatus.CONFLICT,
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
