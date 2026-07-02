"""
Connection Domain Enums

Purpose:
- Define business enums related to ServiceNow connections.
- Provide type-safe connection status values.

This module DOES NOT:
- Contain business logic.
- Interact with the database.
- Perform API calls.
"""

from enum import Enum

# ============================================================
# Connection Status
# ============================================================


class ConnectionStatus(str, Enum):
    """
    Represents the current state of a ServiceNow connection.
    """

    ACTIVE = "ACTIVE"

    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"

    INSTANCE_UNREACHABLE = "INSTANCE_UNREACHABLE"

    DISABLED = "DISABLED"
