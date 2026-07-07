"""
Password Security Utilities

Purpose:
- Hash plain-text passwords.
- Verify passwords against stored hashes.
- Provide a reusable password security layer.

This module DOES NOT:
- Generate JWT tokens.
- Authenticate users.
- Access the database.
"""

from pwdlib import PasswordHash

# ============================================================
# Password Hasher
# ============================================================

password_hasher = PasswordHash.recommended()

# ============================================================
# Password Hashing
# ============================================================


def hash_password(password: str) -> str:
    """
    Hash a plain-text password using Argon2id.

    Args:
        password:
            Plain-text password.

    Returns:
        Secure password hash.
    """

    return password_hasher.hash(password)


# ============================================================
# Password Verification
# ============================================================


def verify_password(
    password: str,
    password_hash: str,
) -> bool:
    """
    Verify a plain-text password against its stored hash.

    Args:
        password:
            Plain-text password.

        password_hash:
            Stored password hash.

    Returns:
        True if the password is valid, otherwise False.
    """

    return password_hasher.verify(
        password,
        password_hash,
    )
