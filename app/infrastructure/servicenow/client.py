"""
ServiceNow Client

Purpose:
- Communicate with the ServiceNow REST API.
- Manage authentication.
- Manage HTTP client configuration.
"""

import httpx

from app.core.config import settings
from app.core.logging import get_logger
from app.exceptions.servicenow import ServiceNowAPIError, ServiceNowAuthenticationError
from app.infrastructure.servicenow.constants import (
    DEFAULT_HEADERS,
    DEFAULT_TIMEOUT,
    HTTP_POST,
)
from app.infrastructure.servicenow.endpoints import INCIDENT
from app.infrastructure.servicenow.models import (
    IncidentCreateRequest,
    IncidentCreateResponse,
)

logger = get_logger(__name__)


# ============================================================
# ServiceNow Client
# ============================================================


class ServiceNowClient:
    """
    Client responsible for communicating
    with the ServiceNow REST API.
    """

    def __init__(self) -> None:
        """
        Initialize the ServiceNow client.
        """

        logger.info("Initializing ServiceNow client.")

        self._base_url = settings.servicenow.url
        self._username = settings.servicenow.username
        self._password = settings.servicenow.password

        self._client = httpx.Client(
            base_url=self._base_url,
            auth=(self._username, self._password),
            headers=DEFAULT_HEADERS,
            timeout=DEFAULT_TIMEOUT,
        )

        logger.info("ServiceNow client initialized.")

    # ============================================================
    # Generic Request
    # ============================================================

    def _request(
        self,
        method: str,
        endpoint: str,
        json: dict | None = None,
    ) -> httpx.Response:
        """
        Execute an HTTP request to ServiceNow.
        """

        logger.info(
            "ServiceNow Request | %s %s",
            method,
            endpoint,
        )

        try:
            response = self._client.request(
                method=method,
                url=endpoint,
                json=json,
            )

        except httpx.TimeoutException as exc:
            logger.exception("ServiceNow request timed out.")

            raise ServiceNowAPIError("ServiceNow request timed out.") from exc

        except httpx.HTTPError as exc:
            logger.exception("ServiceNow HTTP request failed.")

            raise ServiceNowAPIError("ServiceNow HTTP request failed.") from exc

        if response.status_code == 401:
            raise ServiceNowAuthenticationError()

        if response.is_error:
            raise ServiceNowAPIError(
                f"ServiceNow returned HTTP {response.status_code}."
            )

        logger.info(
            "ServiceNow Response | %s",
            response.status_code,
        )

        return response

    # ============================================================
    # Incident Operations
    # ============================================================

    def create_incident(
        self,
        incident: IncidentCreateRequest,
    ) -> IncidentCreateResponse:
        """
        Create a new incident in ServiceNow.
        """

        logger.info("Creating ServiceNow incident.")

        response = self._request(
            method=HTTP_POST,
            endpoint=INCIDENT,
            json=incident.model_dump(
                exclude_none=True,
            ),
        )

        result = response.json()["result"]

        logger.info(
            "Incident %s created successfully.",
            result["number"],
        )

        return IncidentCreateResponse(
            number=result["number"],
            sys_id=result["sys_id"],
            short_description=result["short_description"],
        )
