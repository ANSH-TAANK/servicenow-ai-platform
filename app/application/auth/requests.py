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
    EMAIL_MAX_LENGTH,
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

    Supports authentication using either
    an email address or username.
    """

    identifier: str = Field(
        min_length=1,
        max_length=max(
            EMAIL_MAX_LENGTH,
            USERNAME_MAX_LENGTH,
        ),
        description="Username or email address.",
        examples=[
            "john.doe",
            "john.doe@example.com",
        ],
    )

    password: str = Field(
        min_length=PASSWORD_MIN_LENGTH,
        max_length=PASSWORD_MAX_LENGTH,
        description="User account password.",
        examples=[
            "SecurePassword@123",
        ],
    )


# ============================================================
# Update Username Request
# ============================================================


class UpdateUsernameRequest(RequestModel):
    """
    Request body for updating a user's username.
    """

    username: str = Field(
        min_length=3,
        max_length=USERNAME_MAX_LENGTH,
        description="New unique platform username.",
        examples=[
            "anshtaank",
        ],
    )


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


# ============================================================
# Verify Email Request
# ============================================================


class VerifyEmailRequest(RequestModel):
    """
    Request body for verifying
    a user's email address.
    """

    email: EmailStr

    verification_code: str = Field(
        min_length=6,
        max_length=6,
        description="Six-digit email verification code.",
        examples=[
            "482731",
        ],
    )


# ============================================================
# Resend Verification Request
# ============================================================


class ResendVerificationRequest(RequestModel):
    """
    Request body for requesting
    a new email verification code.
    """

    email: EmailStr


# ============================================================
# Forgot Password Request
# ============================================================


class ForgotPasswordRequest(RequestModel):
    """
    Request body for requesting
    a password reset code.
    """

    email: EmailStr


# ============================================================
# Verify Reset OTP Request
# ============================================================


class VerifyResetOTPRequest(RequestModel):
    """
    Request body for verifying
    a password reset code.
    """

    email: EmailStr

    verification_code: str = Field(
        min_length=6,
        max_length=6,
        description="Six-digit password reset code.",
        examples=[
            "482731",
        ],
    )


# ============================================================
# Reset Password Request
# ============================================================


class ResetPasswordRequest(RequestModel):
    """
    Request body for resetting
    a user's password.
    """

    email: EmailStr

    verification_code: str = Field(
        min_length=6,
        max_length=6,
        description="Verified password reset code.",
        examples=[
            "482731",
        ],
    )

    new_password: str = Field(
        min_length=PASSWORD_MIN_LENGTH,
        max_length=PASSWORD_MAX_LENGTH,
    )
