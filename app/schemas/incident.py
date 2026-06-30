"""
Incident API Schemas

Purpose:
- Define request and response models
  exposed through the REST API.
"""

from pydantic import BaseModel, Field

# ============================================================
# Create Incident Request
# ============================================================


class CreateIncidentRequestSchema(BaseModel):
    """
    API request for creating
    a ServiceNow incident.
    """

    issue: str = Field(
        ...,
        min_length=5,
        max_length=5000,
        examples=[
            "My VPN is not connecting.",
        ],
    )


# ============================================================
# Incident Response Schema
# ============================================================


class IncidentSchema(BaseModel):
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


class CreateIncidentResponseSchema(BaseModel):
    """
    API response returned after
    incident creation.
    """

    success: bool

    message: str

    incident: IncidentSchema
