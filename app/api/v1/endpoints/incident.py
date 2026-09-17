"""
Incident API Endpoints

Purpose:

- Expose REST endpoints for
  ServiceNow incident operations.
"""

from fastapi import APIRouter, Depends, status

from app.api.dependencies.incident import get_incident_service, require_incident_access
from app.application.incident.mappers import (
    map_api_request_to_application,
    map_application_response_to_api,
)
from app.application.incident.service import IncidentService
from app.core.logging import get_logger
from app.infrastructure.database.models.user import User
from app.schemas.incident import (
    CreateIncidentRequestSchema,
    CreateIncidentResponseSchema,
)

logger = get_logger(__name__)


# ============================================================
# Router
# ============================================================


router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"],
)


# ============================================================
# Create Incident
# ============================================================


@router.post(
    "",
    response_model=CreateIncidentResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create Incident",
    description=("Create a ServiceNow incident from a natural language issue."),
)
async def create_incident(
    request: CreateIncidentRequestSchema,
    service: IncidentService = Depends(
        get_incident_service,
    ),
    user: User = Depends(
        require_incident_access,
    ),
) -> CreateIncidentResponseSchema:
    """
    Create a ServiceNow incident.
    """

    logger.info(
        "Received incident creation request from user %s.",
        user.id,
    )

    application_request = map_api_request_to_application(
        request,
    )

    application_response = await service.create_incident(
        application_request,
        user_email=user.email,
        user_full_name=user.full_name,
    )

    logger.info(
        "Incident %s created successfully.",
        application_response.incident.incident_number,
    )

    return map_application_response_to_api(
        application_response,
    )
