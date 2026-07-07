"""
Authentication Response Models

Purpose:
- Define authentication response schemas.
- Represent authentication responses.

This module DOES NOT:
- Authenticate users.
- Access the database.
- Generate JWT tokens.
"""

from uuid import UUID

from pydantic import BaseModel, ConfigDict

# ============================================================
# Base Response Model
# ============================================================


class ResponseModel(BaseModel):
    """
    Base response model.

    All authentication response models inherit
    from this class.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )


# ============================================================
# User Response
# ============================================================


class UserResponse(ResponseModel):
    """
    User information returned to clients.
    """

    id: UUID

    username: str

    full_name: str

    email: str

    is_active: bool


# ============================================================
# Login Response
# ============================================================


class LoginResponse(ResponseModel):
    """
    Authentication token response.
    """

    access_token: str

    refresh_token: str

    token_type: str


# ============================================================
# Refresh Token Response
# ============================================================


class RefreshTokenResponse(ResponseModel):
    """
    Refresh token response.
    """

    access_token: str

    refresh_token: str

    token_type: str
