"""
ServiceNow Models

Purpose:
- Define request and response models used by the
  ServiceNow client.
"""

from pydantic import BaseModel

# ============================================================
# Incident Create Request
# ============================================================


class IncidentCreateRequest(BaseModel):
    """
    Request payload for creating
    a ServiceNow incident.
    """

    short_description: str

    description: str

    category: str | None = None

    subcategory: str | None = None

    assignment_group: str | None = None

    impact: str | None = None

    urgency: str | None = None

    caller_id: str | None = None


# ============================================================
# Incident Create Response
# ============================================================


class IncidentCreateResponse(BaseModel):
    """
    Response returned after
    creating an incident.
    """

    number: str

    sys_id: str

    short_description: str


# ============================================================
# Generic Table Response
# ============================================================


class TableResponse(BaseModel):
    """
    Generic ServiceNow Table API response.
    """

    result: dict


# ============================================================
# ServiceNow User
# ============================================================


class ServiceNowUser(BaseModel):
    """
    Internal representation of a
    ServiceNow user.
    """

    sys_id: str

    username: str

    email: str

    first_name: str | None = None

    last_name: str | None = None

    active: bool = True


# ============================================================
# Approval Create Request
# ============================================================


class ApprovalRequestCreate(BaseModel):
    """
    Request payload for creating
    a ServiceNow approval request.
    """

    first_name: str

    last_name: str

    username: str

    email: str

    fastapi_user_id: str

    access_justification: str | None = None


# ============================================================
# Approval Create Response
# ============================================================


class ApprovalRequestCreateResponse(BaseModel):
    """
    Response returned after
    creating an approval request.
    """

    sys_id: str

    number: str


# ============================================================
# ServiceNow Approval Request
# ============================================================


class ApprovalRequest(BaseModel):
    """
    Internal representation of a
    ServiceNow approval request.
    """

    sys_id: str

    number: str

    approval_status: str

    callback_status: str

    user_creation_status: str

    first_name: str

    last_name: str

    username: str

    email: str

    fastapi_user_id: str

    access_justification: str | None = None

    approved_at: str | None = None

    rejected_at: str | None = None

    rejection_reason: str | None = None
