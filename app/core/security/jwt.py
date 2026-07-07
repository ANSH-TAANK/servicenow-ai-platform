"""
JWT Security Utilities

Purpose:
- Create JWT access tokens.
- Create JWT refresh tokens.
- Decode and validate JWT tokens.

This module DOES NOT:
- Authenticate users.
- Access the database.
- Know about FastAPI.
"""

from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import uuid4

import jwt
from jwt import ExpiredSignatureError
from jwt import InvalidTokenError as JWTInvalidTokenError

from app.core.config import settings
from app.core.constants import (
    ACCESS_TOKEN_TYPE,
    JWT_EXP,
    JWT_IAT,
    JWT_JTI,
    JWT_SUBJECT,
    JWT_TYPE,
    REFRESH_TOKEN_TYPE,
)
from app.core.security.exceptions import (
    ExpiredTokenError,
    InvalidTokenError,
    InvalidTokenTypeError,
)

# ============================================================
# Internal Token Creation
# ============================================================


def _create_token(
    *,
    subject: str,
    token_type: str,
    secret: str,
    expires_delta: timedelta,
) -> str:
    """
    Create a JWT token.

    Args:
        subject:
            User UUID.

        token_type:
            Token type ("access" or "refresh").

        secret:
            Secret key used to sign the token.

        expires_delta:
            Token lifetime.

    Returns:
        Encoded JWT token.
    """

    now = datetime.now(UTC)

    payload = {
        JWT_SUBJECT: subject,
        JWT_TYPE: token_type,
        JWT_JTI: str(uuid4()),
        JWT_IAT: now,
        JWT_EXP: now + expires_delta,
    }

    return jwt.encode(
        payload,
        secret,
        algorithm=settings.security.jwt_algorithm,
    )


# ============================================================
# Access Token
# ============================================================


def create_access_token(
    subject: str,
) -> str:
    """
    Create a JWT access token.
    """

    return _create_token(
        subject=subject,
        token_type=ACCESS_TOKEN_TYPE,
        secret=settings.security.access_token_secret,
        expires_delta=timedelta(
            minutes=settings.security.access_token_expire_minutes,
        ),
    )


# ============================================================
# Refresh Token
# ============================================================


def create_refresh_token(
    subject: str,
) -> str:
    """
    Create a JWT refresh token.
    """

    return _create_token(
        subject=subject,
        token_type=REFRESH_TOKEN_TYPE,
        secret=settings.security.refresh_token_secret,
        expires_delta=timedelta(
            days=settings.security.refresh_token_expire_days,
        ),
    )


# ============================================================
# Internal Token Decoding
# ============================================================


def _decode_token(
    *,
    token: str,
    secret: str,
    expected_type: str,
) -> dict[str, Any]:
    """
    Decode and validate a JWT token.

    Args:
        token:
            JWT token.

        secret:
            Secret used to verify the token.

        expected_type:
            Expected JWT type.

    Returns:
        Decoded payload.

    Raises:
        ExpiredTokenError:
            If the token has expired.

        InvalidTokenError:
            If the token is invalid.

        InvalidTokenTypeError:
            If the token type does not match.
    """

    try:
        payload = jwt.decode(
            token,
            secret,
            algorithms=[
                settings.security.jwt_algorithm,
            ],
        )

    except ExpiredSignatureError as exc:
        raise ExpiredTokenError() from exc

    except JWTInvalidTokenError as exc:
        raise InvalidTokenError() from exc

    if payload.get(JWT_TYPE) != expected_type:
        raise InvalidTokenTypeError()

    return payload


# ============================================================
# Access Token Decoding
# ============================================================


def decode_access_token(
    token: str,
) -> dict[str, Any]:
    """
    Decode an access token.
    """

    return _decode_token(
        token=token,
        secret=settings.security.access_token_secret,
        expected_type=ACCESS_TOKEN_TYPE,
    )


# ============================================================
# Refresh Token Decoding
# ============================================================


def decode_refresh_token(
    token: str,
) -> dict[str, Any]:
    """
    Decode a refresh token.
    """

    return _decode_token(
        token=token,
        secret=settings.security.refresh_token_secret,
        expected_type=REFRESH_TOKEN_TYPE,
    )
