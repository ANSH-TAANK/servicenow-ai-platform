"""
Approval Domain Enums

Purpose:
- Define approval states for user onboarding.
- Define how a user was approved.

This module DOES NOT:
- Store approval records.
- Perform approval logic.
- Interact with the database.
"""

from enum import Enum

# ============================================================
# Approval Status
# ============================================================


class ApprovalStatus(str, Enum):
    """
    Represents the current approval status of a user.
    """

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


# ============================================================
# Approval Type
# ============================================================


class ApprovalType(str, Enum):
    """
    Represents how the approval was granted.
    """

    MANUAL = "manual"
    AUTO = "auto"
