"""
OTP Security Utilities

Purpose:
- Generate secure verification codes.
- Hash verification codes.
- Verify verification codes against stored hashes.

This module DOES NOT:
- Access the database.
- Send emails.
- Track verification attempts.
- Generate expiration timestamps.
"""

from secrets import randbelow

from pwdlib import PasswordHash

from app.core.constants import OTP_LENGTH

# ============================================================
# OTP Hasher
# ============================================================

otp_hasher = PasswordHash.recommended()

# ============================================================
# OTP Generation
# ============================================================


def generate_verification_code() -> str:
    """
    Generate a secure numeric verification code.

    Returns:
        A zero-padded verification code.
    """

    maximum = 10**OTP_LENGTH

    return f"{randbelow(maximum):0{OTP_LENGTH}d}"


# ============================================================
# OTP Hashing
# ============================================================


def hash_verification_code(
    verification_code: str,
) -> str:
    """
    Hash a verification code using Argon2id.

    Args:
        verification_code:
            Plain-text verification code.

    Returns:
        Secure verification code hash.
    """

    return otp_hasher.hash(
        verification_code,
    )


# ============================================================
# OTP Verification
# ============================================================


def verify_verification_code(
    verification_code: str,
    verification_code_hash: str,
) -> bool:
    """
    Verify a verification code against its stored hash.

    Args:
        verification_code:
            Plain-text verification code.

        verification_code_hash:
            Stored verification code hash.

    Returns:
        True if the verification code is valid,
        otherwise False.
    """

    return otp_hasher.verify(
        verification_code,
        verification_code_hash,
    )
