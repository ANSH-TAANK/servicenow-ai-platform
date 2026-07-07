"""
Authentication Validators

Purpose:
- Validate authentication business rules.
- Normalize authentication input.

This module DOES NOT:
- Access the database.
- Authenticate users.
- Generate JWT tokens.
"""

import re

from app.application.auth.exceptions import InvalidPasswordError, InvalidUsernameError
from app.core.constants import (
    PASSWORD_DIGIT_PATTERN,
    PASSWORD_LOWERCASE_PATTERN,
    PASSWORD_SPECIAL_CHARACTER_PATTERN,
    PASSWORD_UPPERCASE_PATTERN,
    RESERVED_USERNAMES,
    USERNAME_PATTERN,
)

# ============================================================
# Email
# ============================================================


def normalize_email(
    email: str,
) -> str:
    """
    Normalize an email address.

    Args:
        email:
            User email.

    Returns:
        Normalized email.
    """

    return email.lower()


# ============================================================
# Username
# ============================================================


def normalize_username(
    username: str,
) -> str:
    """
    Normalize a username.

    Args:
        username:
            User username.

    Returns:
        Normalized username.
    """

    return username.lower()


# ============================================================
# Username
# ============================================================


def validate_username(
    username: str,
) -> None:
    """
    Validate a username.

    Args:
        username:
            Username to validate.

    Raises:
        InvalidUsernameError:
            If the username is invalid.
    """

    if username.lower() in RESERVED_USERNAMES:
        raise InvalidUsernameError(
            "Username is reserved.",
        )

    if not re.fullmatch(
        USERNAME_PATTERN,
        username,
    ):
        raise InvalidUsernameError(
            ("Username may contain only " "letters, numbers, and underscores."),
        )


# ============================================================
# Password
# ============================================================


def validate_password(
    password: str,
) -> None:
    """
    Validate a password.

    Args:
        password:
            Password to validate.

    Raises:
        InvalidPasswordError:
            If the password is invalid.
    """

    if not re.search(
        PASSWORD_UPPERCASE_PATTERN,
        password,
    ):
        raise InvalidPasswordError(
            ("Password must contain at least " "one uppercase letter."),
        )

    if not re.search(
        PASSWORD_LOWERCASE_PATTERN,
        password,
    ):
        raise InvalidPasswordError(
            ("Password must contain at least " "one lowercase letter."),
        )

    if not re.search(
        PASSWORD_DIGIT_PATTERN,
        password,
    ):
        raise InvalidPasswordError(
            ("Password must contain at least " "one digit."),
        )

    if not re.search(
        PASSWORD_SPECIAL_CHARACTER_PATTERN,
        password,
    ):
        raise InvalidPasswordError(
            ("Password must contain at least " "one special character."),
        )
