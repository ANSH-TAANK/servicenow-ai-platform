"""
Incident Dependencies

Purpose:
- Provide IncidentService instances.
"""

from app.api.dependencies.ai import get_ai_provider_dependency
from app.api.dependencies.servicenow import get_servicenow_client
from app.application.incident.service import IncidentService

# ============================================================
# Incident Service Dependency
# ============================================================


def get_incident_service() -> IncidentService:
    """
    Return an IncidentService instance.
    """

    provider = get_ai_provider_dependency()

    servicenow = get_servicenow_client()

    return IncidentService(
        provider=provider,
        servicenow=servicenow,
    )
