"""
Password Security Tests

Purpose:
- Verify password hashing.
- Verify password validation.
- Ensure plain-text passwords are never stored.
"""

from app.core.security import hash_password, verify_password

# ============================================================
# Password Security Tests
# ============================================================


class TestPasswordSecurity:
    """
    Unit tests for password security utilities.
    """

    # ============================================================
    # Password Hashing
    # ============================================================

    def test_hash_password(self) -> None:
        """
        Verify that a password is securely hashed.
        """

        password = "MySecurePassword123!"

        password_hash = hash_password(password)

        assert password_hash != password
        assert isinstance(password_hash, str)
        assert len(password_hash) > 0

    # ============================================================
    # Password Verification
    # ============================================================

    def test_verify_password_success(self) -> None:
        """
        Verify that a valid password is accepted.
        """

        password = "MySecurePassword123!"

        password_hash = hash_password(password)

        assert verify_password(
            password,
            password_hash,
        )

    # ============================================================
    # Invalid Password
    # ============================================================

    def test_verify_password_failure(self) -> None:
        """
        Verify that an invalid password is rejected.
        """

        password_hash = hash_password(
            "MySecurePassword123!",
        )

        assert not verify_password(
            "WrongPassword123!",
            password_hash,
        )
