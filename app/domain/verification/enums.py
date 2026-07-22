"""
Verification Domain Enums

Purpose:
- Define verification-related enumerations.
- Keep verification states type-safe.
- Avoid magic strings across the application.

This module DOES NOT:
- Contain business logic.
- Interact with the database.
"""

from enum import StrEnum

# ============================================================
# Verification Purpose
# ============================================================


class VerificationPurpose(StrEnum):
    """
    Represents the purpose of a verification request.
    """

    EMAIL_VERIFICATION = "email_verification"

    PASSWORD_RESET = "password_reset"

    EMAIL_CHANGE = "email_change"


# ============================================================
# Verification Method
# ============================================================


class VerificationMethod(StrEnum):
    """
    Represents how verification is performed.
    """

    EMAIL = "email"

    SMS = "sms"


# ============================================================
# Verification Status
# ============================================================


class VerificationStatus(StrEnum):
    """
    Represents the verification lifecycle.
    """

    PENDING = "pending"

    VERIFIED = "verified"

    EXPIRED = "expired"

    FAILED = "failed"
