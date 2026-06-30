"""
Incident Application Responses

Purpose:
- Define responses returned by the
  Incident Application Service.
"""

from pydantic import BaseModel, Field

# ============================================================
# Incident Details
# ============================================================


class IncidentDetails(BaseModel):
    """
    Details of the created incident.
    """

    incident_number: str

    incident_sys_id: str

    short_description: str

    description: str

    category: str

    subcategory: str

    assignment_group: str

    impact: str

    urgency: str


# ============================================================
# Create Incident Response
# ============================================================


class CreateIncidentResponse(BaseModel):
    """
    Response returned after successfully
    creating a ServiceNow incident.
    """

    success: bool = True

    message: str = Field(
        default="Incident created successfully.",
    )

    incident: IncidentDetails
