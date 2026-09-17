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
from app.infrastructure.email.models import EmailMessage
from app.infrastructure.email.service import EmailService
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
        email_service: EmailService,
    ) -> None:
        """
        Initialize the service with its dependencies.
        """

        self._provider = provider
        self._servicenow = servicenow
        self._email_service = email_service

    # ========================================================
    # Create Incident
    # ========================================================

    async def create_incident(
        self,
        request: CreateIncidentRequest,
        *,
        user_email: str,
        user_full_name: str,
    ) -> CreateIncidentResponse:
        """
        Create a ServiceNow incident from a
        natural language issue description.

        The incident is created first. Once the incident
        is successfully created, a confirmation email is
        sent to the verified platform user's email address.
        """

        logger.info(
            "Starting incident creation workflow.",
        )

        # ----------------------------------------------------
        # Validate request
        # ----------------------------------------------------

        validate_create_incident_request(
            request,
        )

        logger.info(
            "Incident request validated.",
        )

        # ----------------------------------------------------
        # Build AI Request
        # ----------------------------------------------------

        ai_request = AIProviderRequest(
            issue=request.issue,
        )

        # ----------------------------------------------------
        # AI Prediction
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # Map Prediction
        # ----------------------------------------------------

        servicenow_request = map_prediction_to_servicenow_request(
            prediction=ai_response,
            caller_id=request.caller_id,
        )

        logger.info(
            "Prediction mapped to ServiceNow request.",
        )

        # ----------------------------------------------------
        # Create ServiceNow Incident
        # ----------------------------------------------------

        incident = self._servicenow.create_incident(
            servicenow_request,
        )

        logger.info(
            "Incident %s created successfully.",
            incident.number,
        )

        # ----------------------------------------------------
        # Build Application Response
        # ----------------------------------------------------

        response = CreateIncidentResponse(
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

        # ----------------------------------------------------
        # Send Incident Confirmation Email
        # ----------------------------------------------------

        try:
            await self._send_incident_confirmation_email(
                response=response,
                user_email=user_email,
                user_full_name=user_full_name,
            )

        except Exception:
            logger.exception(
                "Failed to send incident confirmation email " "for incident %s.",
                incident.number,
            )

            # IMPORTANT:
            # The incident was already created successfully.
            # Email failure must not turn the successful
            # incident creation into an API failure.

        # ----------------------------------------------------
        # Return Existing Response
        # ----------------------------------------------------

        return response

    # ========================================================
    # Incident Confirmation Email
    # ========================================================

    async def _send_incident_confirmation_email(
        self,
        *,
        response: CreateIncidentResponse,
        user_email: str,
        user_full_name: str,
    ) -> None:
        """
        Send a confirmation email containing the
        successfully created incident details.
        """

        incident = response.incident

        email_message = EmailMessage(
            to_email=user_email,
            subject=(f"Incident {incident.incident_number} " "Created Successfully"),
            template="incident_created.html",
            context={
                "full_name": user_full_name,
                "incident_number": incident.incident_number,
                "short_description": incident.short_description,
                "description": incident.description,
                "category": incident.category,
                "subcategory": incident.subcategory,
                "assignment_group": incident.assignment_group,
                "impact": incident.impact,
                "urgency": incident.urgency,
            },
        )

        result = await self._email_service.send_email(
            email_message,
        )

        if not result.success:
            logger.warning(
                "Incident confirmation email was not sent "
                "for incident %s. Provider: %s, Error: %s",
                incident.incident_number,
                result.provider,
                result.error,
            )

            return

        logger.info(
            "Incident confirmation email sent successfully " "for incident %s to %s.",
            incident.incident_number,
            user_email,
        )
