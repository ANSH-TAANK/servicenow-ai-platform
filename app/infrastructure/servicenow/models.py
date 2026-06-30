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
