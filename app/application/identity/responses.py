"""
Identity Responses

Purpose:
- Define application-layer response models
  for identity management workflows.

This module DOES NOT:
- Access the database.
- Call ServiceNow APIs.
- Perform provisioning.
"""

from uuid import UUID

from pydantic import BaseModel

from app.domain.enums.identity import IdentityStatus

# ============================================================
# Verify Identity Response
# ============================================================


class VerifyIdentityResponse(BaseModel):
    """
    Result of verifying a platform user's
    ServiceNow identity.
    """

    user_id: UUID

    status: IdentityStatus

    servicenow_sys_id: str | None = None

    servicenow_username: str | None = None

    servicenow_email: str | None = None

    message: str
