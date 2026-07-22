"""
ServiceNow User Service

Purpose:
- Manage ServiceNow user operations.
- Encapsulate all interactions with the ServiceNow sys_user table.
"""

from app.core.logging import get_logger
from app.infrastructure.servicenow.client import ServiceNowClient
from app.infrastructure.servicenow.endpoints import USER
from app.infrastructure.servicenow.models import ServiceNowUser

logger = get_logger(__name__)

# ============================================================
# ServiceNow User Fields
# ============================================================

USER_FIELDS = ",".join(
    (
        "sys_id",
        "user_name",
        "email",
        "first_name",
        "last_name",
        "active",
    )
)

# ============================================================
# ServiceNow User Service
# ============================================================


class ServiceNowUserService:
    """
    Service responsible for managing
    ServiceNow user operations.
    """

    def __init__(
        self,
        client: ServiceNowClient,
    ) -> None:
        """
        Initialize the ServiceNow user service.
        """

        self._client = client

    # ============================================================
    # Find User by Email
    # ============================================================

    def find_by_email(
        self,
        email: str,
    ) -> ServiceNowUser | None:
        """
        Retrieve a ServiceNow user by email.

        Returns:
            ServiceNowUser if found, otherwise None.
        """

        logger.info(
            "Searching ServiceNow user by email '%s'.",
            email,
        )

        params = {
            "sysparm_query": f"email={email}",
            "sysparm_fields": USER_FIELDS,
        }

        response = self._client.get(
            endpoint=USER,
            params=params,
        )

        result = response.json()["result"]

        if not result:

            logger.info(
                "No ServiceNow user found for email '%s'.",
                email,
            )

            return None

        logger.info(
            "ServiceNow user found for email '%s'.",
            email,
        )

        return self._map_user(
            result[0],
        )

    # ============================================================
    # Map ServiceNow User
    # ============================================================

    def _map_user(
        self,
        data: dict,
    ) -> ServiceNowUser:
        """
        Convert a ServiceNow user record into
        a ServiceNowUser model.
        """

        return ServiceNowUser(
            sys_id=data["sys_id"],
            username=data["user_name"],
            email=data["email"],
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            active=data.get("active", "true") == "true",
        )
