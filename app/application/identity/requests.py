"""
Identity Requests

Purpose:
- Define application-layer request models
  for identity management workflows.

This module DOES NOT:
- Validate HTTP requests.
- Access the database.
- Call ServiceNow APIs.
"""

from uuid import UUID

from pydantic import BaseModel

# ============================================================
# Verify ServiceNow Identity
# ============================================================


class VerifyIdentityRequest(BaseModel):
    """
    Verify whether a platform user
    exists in ServiceNow.
    """

    user_id: UUID


# ============================================================
# Synchronize ServiceNow Identity
# ============================================================


class SynchronizeIdentityRequest(BaseModel):
    """
    Synchronize a platform user with
    an existing ServiceNow identity.
    """

    user_id: UUID


# ============================================================
# Request ServiceNow Provisioning
# ============================================================


class ProvisionIdentityRequest(BaseModel):
    """
    Request creation of a new
    ServiceNow user.
    """

    user_id: UUID
