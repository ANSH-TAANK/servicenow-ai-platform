"""
API Mapper

Purpose:
- Convert API schemas to application models.
- Convert application models to API schemas.
"""

from app.application.incident.requests import CreateIncidentRequest
from app.application.incident.responses import CreateIncidentResponse
from app.schemas.incident import (
    CreateIncidentRequestSchema,
    CreateIncidentResponseSchema,
    IncidentSchema,
)

# ============================================================
# API Request Mapper
# ============================================================


def map_api_request_to_application(
    request: CreateIncidentRequestSchema,
) -> CreateIncidentRequest:
    """
    Convert an API request into an
    application request.
    """

    return CreateIncidentRequest(
        issue=request.issue,
    )


# ============================================================
# API Response Mapper
# ============================================================


def map_application_response_to_api(
    response: CreateIncidentResponse,
) -> CreateIncidentResponseSchema:
    """
    Convert an application response into
    an API response.
    """

    return CreateIncidentResponseSchema(
        success=response.success,
        message=response.message,
        incident=IncidentSchema(
            incident_number=response.incident.incident_number,
            incident_sys_id=response.incident.incident_sys_id,
            short_description=response.incident.short_description,
            description=response.incident.description,
            category=response.incident.category,
            subcategory=response.incident.subcategory,
            assignment_group=response.incident.assignment_group,
            impact=response.incident.impact,
            urgency=response.incident.urgency,
        ),
    )
