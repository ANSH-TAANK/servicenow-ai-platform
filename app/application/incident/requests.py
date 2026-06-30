"""
Incident Application Requests

Purpose:
- Define requests accepted by the
  Incident Application Service.
"""

from pydantic import BaseModel, Field

# ============================================================
# Create Incident Request
# ============================================================


class CreateIncidentRequest(BaseModel):
    """
    Request for creating a new incident.
    """

    issue: str = Field(
        ...,
        min_length=5,
        max_length=5000,
        description="Natural language issue description.",
    )

    caller_id: str | None = Field(
        default=None,
        description="Optional ServiceNow caller sys_id.",
    )
