"""
Authentication Request Models

Purpose:
- Define authentication request schemas.
- Validate incoming authentication data.

This module DOES NOT:
- Authenticate users.
- Access the database.
- Generate JWT tokens.
"""

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.core.constants import (
    NAME_MAX_LENGTH,
    PASSWORD_MAX_LENGTH,
    PASSWORD_MIN_LENGTH,
    USERNAME_MAX_LENGTH,
)

# ============================================================
# Base Request Model
# ============================================================


class RequestModel(BaseModel):
    """
    Base request model.

    All authentication request models inherit
    from this class.
    """

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )


# ============================================================
# Register Request
# ============================================================


class RegisterRequest(RequestModel):
    """
    Request body for user registration.
    """

    username: str = Field(
        min_length=3,
        max_length=USERNAME_MAX_LENGTH,
    )

    full_name: str = Field(
        min_length=1,
        max_length=NAME_MAX_LENGTH,
    )

    email: EmailStr

    password: str = Field(
        min_length=PASSWORD_MIN_LENGTH,
        max_length=PASSWORD_MAX_LENGTH,
    )


# ============================================================
# Login Request
# ============================================================


class LoginRequest(RequestModel):
    """
    Request body for user login.
    """

    email: EmailStr

    password: str = Field(
        min_length=PASSWORD_MIN_LENGTH,
        max_length=PASSWORD_MAX_LENGTH,
    )


# ============================================================
# OAuth2 Login Request
# ============================================================


# ============================================================
# Refresh Token Request
# ============================================================


class RefreshTokenRequest(RequestModel):
    """
    Request body for refreshing an access token.
    """

    refresh_token: str = Field(
        min_length=1,
    )
