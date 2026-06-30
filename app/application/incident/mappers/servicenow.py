"""
Incident Application Mapper

Purpose:
- Convert AI predictions into
  ServiceNow request models.
"""

from app.infrastructure.ai.models import AIProviderResponse
from app.infrastructure.servicenow.models import IncidentCreateRequest

# ============================================================
# Incident Mapper
# ============================================================


def map_prediction_to_servicenow_request(
    prediction: AIProviderResponse,
    caller_id: str | None = None,
) -> IncidentCreateRequest:
    """
    Convert an AI prediction into a
    ServiceNow incident request.
    """

    incident = prediction.prediction

    return IncidentCreateRequest(
        short_description=incident.short_description,
        description=incident.description,
        category=incident.category,
        subcategory=incident.subcategory,
        assignment_group=incident.assignment_group,
        impact=incident.impact.value,
        urgency=incident.urgency.value,
        caller_id=caller_id,
    )
