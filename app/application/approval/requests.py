"""
Approval Request Models

Purpose:
- Define request models for approval workflows.
- Validate incoming approval-related requests.
- Represent the contract between external systems
  and the application.

This module DOES NOT:
- Contain business logic.
- Access the database.
- Call ServiceNow APIs.
"""

# Standard Library Imports
from typing import Literal
from uuid import UUID

# Third-Party Imports
from pydantic import BaseModel, ConfigDict, Field

# ============================================================
# Approval Callback Request
# ============================================================


class ApprovalCallbackRequest(BaseModel):
    """
    Request model for approval callbacks received from ServiceNow.

    This model represents the webhook payload sent by ServiceNow
    after an approval request is approved or rejected.
    """

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    fastapi_user_id: UUID = Field(
        ...,
        description="Unique identifier of the FastAPI user.",
    )

    action: Literal["approved", "rejected"] = Field(
        ..., description="Approval decision made in ServiceNow."
    )

    approval_request_number: str = Field(
        ...,
        min_length=1,
        description="ServiceNow approval request number.",
    )

    servicenow_user_sys_id: str | None = Field(
        default=None,
        description="ServiceNow User sys_id. Present only for approved requests.",
    )

    reason: str | None = Field(
        default=None,
        description="Optional reason for rejection.",
    )
