"""
JWT Security Tests

Purpose:
- Verify JWT creation.
- Verify JWT decoding.
- Validate token payload contents.
"""

import uuid

import pytest

from app.core.constants import (
    ACCESS_TOKEN_TYPE,
    JWT_EXP,
    JWT_IAT,
    JWT_JTI,
    JWT_SUBJECT,
    JWT_TYPE,
    REFRESH_TOKEN_TYPE,
)
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_access_token,
    decode_refresh_token,
)
from app.core.security.exceptions import InvalidTokenError

# ============================================================
# JWT Security Tests
# ============================================================


class TestJWTSecurity:
    """
    Unit tests for JWT utilities.
    """

    # ============================================================
    # Access Token
    # ============================================================

    def test_create_access_token(self) -> None:
        """
        Verify that an access token is created and decoded correctly.
        """

        user_id = str(uuid.uuid4())

        token = create_access_token(user_id)

        payload = decode_access_token(token)

        assert payload[JWT_SUBJECT] == user_id
        assert payload[JWT_TYPE] == ACCESS_TOKEN_TYPE

        assert JWT_JTI in payload
        assert JWT_IAT in payload
        assert JWT_EXP in payload

    # ============================================================
    # Refresh Token
    # ============================================================

    def test_create_refresh_token(self) -> None:
        """
        Verify that a refresh token is created and decoded correctly.
        """

        user_id = str(uuid.uuid4())

        token = create_refresh_token(user_id)

        payload = decode_refresh_token(token)

        assert payload[JWT_SUBJECT] == user_id
        assert payload[JWT_TYPE] == REFRESH_TOKEN_TYPE

        assert JWT_JTI in payload
        assert JWT_IAT in payload
        assert JWT_EXP in payload

    # ============================================================
    # Invalid Access Token
    # ============================================================

    def test_invalid_access_token(self) -> None:
        """
        Verify that a refresh token cannot be decoded
        as an access token.
        """

        user_id = str(uuid.uuid4())

        token = create_refresh_token(user_id)

        with pytest.raises(InvalidTokenError):
            decode_access_token(token)

    # ============================================================
    # Invalid Refresh Token
    # ============================================================

    def test_invalid_refresh_token(self) -> None:
        """
        Verify that an access token cannot be decoded
        as a refresh token.
        """

        user_id = str(uuid.uuid4())

        token = create_access_token(user_id)

        with pytest.raises(InvalidTokenError):
            decode_refresh_token(token)
