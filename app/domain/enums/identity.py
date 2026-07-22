"""
Identity Domain Enums

Purpose:
- Define identity-related domain enumerations.
"""

from enum import Enum

# ============================================================
# Identity Status
# ============================================================


class IdentityStatus(str, Enum):
    """
    Represents the ServiceNow identity state
    of a platform user.
    """

    LINKED = "linked"

    NOT_LINKED = "not_linked"

    PENDING_APPROVAL = "pending_approval"

    REJECTED = "rejected"
