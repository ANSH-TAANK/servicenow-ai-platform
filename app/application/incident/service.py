"""
Incident Application Service

Purpose:
- Orchestrate the complete incident
  creation workflow.
"""

from app.application.incident.mappers import map_prediction_to_servicenow_request
from app.application.incident.requests import CreateIncidentRequest
from app.application.incident.responses import CreateIncidentResponse, IncidentDetails
from app.application.incident.validators import validate_create_incident_request
from app.core.logging import get_logger
from app.domain.incident.short_description import generate_short_description
from app.infrastructure.ai.base import AIProvider
from app.infrastructure.ai.models import AIProviderRequest
from app.infrastructure.servicenow.client import ServiceNowClient

logger = get_logger(__name__)


# ============================================================
# Incident Service
# ============================================================


class IncidentService:
    """
    Application service responsible
    for creating incidents.
    """

    def __init__(
        self,
        provider: AIProvider,
        servicenow: ServiceNowClient,
    ) -> None:
        """
        Initialize the service with its dependencies.
        """

        self._provider = provider
        self._servicenow = servicenow

    # ============================================================
    # Create Incident
    # ============================================================

    def create_incident(
        self,
        request: CreateIncidentRequest,
    ) -> CreateIncidentResponse:
        """
        Create a ServiceNow incident from a
        natural language issue description.
        """

        logger.info("Starting incident creation workflow.")

        # --------------------------------------------------------
        # Validate request
        # --------------------------------------------------------

        validate_create_incident_request(
            request,
        )

        logger.info("Incident request validated.")

        # --------------------------------------------------------
        # Build AI Request
        # --------------------------------------------------------

        ai_request = AIProviderRequest(
            issue=request.issue,
        )

        # --------------------------------------------------------
        # AI Prediction
        # --------------------------------------------------------

        ai_response = self._provider.predict(
            ai_request,
        )

        logger.info(
            "Prediction generated using %s.",
            ai_response.provider.value,
        )

        ai_response.prediction.short_description = generate_short_description(
            category=ai_response.prediction.category,
            subcategory=ai_response.prediction.subcategory,
            description=ai_response.prediction.description,
        )

        logger.info(
            "Standardized short description generated.",
        )

        # --------------------------------------------------------
        # Map prediction
        # --------------------------------------------------------

        servicenow_request = map_prediction_to_servicenow_request(
            prediction=ai_response,
            caller_id=request.caller_id,
        )

        logger.info("Prediction mapped to ServiceNow request.")

        # --------------------------------------------------------
        # Create ServiceNow Incident
        # --------------------------------------------------------

        incident = self._servicenow.create_incident(
            servicenow_request,
        )

        logger.info(
            "Incident %s created successfully.",
            incident.number,
        )

        # --------------------------------------------------------
        # Return Response
        # --------------------------------------------------------

        return CreateIncidentResponse(
            success=True,
            message="Incident created successfully.",
            incident=IncidentDetails(
                incident_number=incident.number,
                incident_sys_id=incident.sys_id,
                short_description=incident.short_description,
                description=ai_response.prediction.description,
                category=ai_response.prediction.category,
                subcategory=ai_response.prediction.subcategory,
                assignment_group=ai_response.prediction.assignment_group,
                impact=ai_response.prediction.impact.value,
                urgency=ai_response.prediction.urgency.value,
            ),
        )
