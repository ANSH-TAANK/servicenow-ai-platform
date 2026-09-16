"""
ServiceNow Approval Service

Purpose:
- Manage ServiceNow approval request operations.
- Encapsulate all interactions with the
  ServiceNow Approval Request table.
"""

from app.core.logging import get_logger
from app.infrastructure.servicenow.client import ServiceNowClient
from app.infrastructure.servicenow.endpoints import APPROVAL_REQUEST, USER
from app.infrastructure.servicenow.models import (
    ApprovalRequest,
    ApprovalRequestCreate,
    ApprovalRequestCreateResponse,
    ServiceNowUser,
)

logger = get_logger(__name__)

# ============================================================
# ServiceNow Approval Fields
# ============================================================

APPROVAL_FIELDS = ",".join(
    (
        "sys_id",
        "number",
        "approval_status",
        "callback_status",
        "user_creation_status",
        "full_name",
        "username",
        "email",
        "fastapi_user_id",
        "access_justification",
        "approved_at",
        "rejected_at",
        "rejection_reason",
    )
)

# ============================================================
# ServiceNow Approval Service
# ============================================================


class ServiceNowApprovalService:
    """
    Service responsible for managing
    ServiceNow approval request operations.
    """

    def __init__(
        self,
        client: ServiceNowClient,
    ) -> None:
        """
        Initialize the approval service.
        """

        self._client = client

    # ============================================================
    # Create Approval Request
    # ============================================================

    def create_request(
        self,
        request: ApprovalRequestCreate,
    ) -> ApprovalRequestCreateResponse:
        """
        Create a ServiceNow approval request.
        """

        logger.info(
            "Creating ServiceNow approval request for '%s'.",
            request.email,
        )

        response = self._client.post(
            endpoint=APPROVAL_REQUEST,
            json=request.model_dump(
                exclude_none=True,
            ),
        )

        result = response.json()["result"]

        logger.info(
            "Approval request %s created successfully.",
            result["number"],
        )

        return self._map_create_response(
            result,
        )

    def find_user_by_email(
        self,
        email: str,
    ) -> ServiceNowUser | None:
        """
        Find a ServiceNow user by email.
        """

        logger.info(
            "Searching ServiceNow user with email '%s'.",
            email,
        )

        response = self._client.get(
            endpoint=USER,
            params={
                "sysparm_query": f"email={email}",
                "sysparm_limit": "1",
                "sysparm_fields": (
                    "sys_id," "user_name," "first_name," "last_name," "email," "active"
                ),
            },
        )

        result = response.json()["result"]

        if not result:
            logger.info(
                "No ServiceNow user found for email '%s'.",
                email,
            )
            return None

        user = result[0]

        logger.info(
            "ServiceNow user '%s' found.",
            user["user_name"],
        )

        return ServiceNowUser(
            sys_id=user["sys_id"],
            username=user["user_name"],
            email=user["email"],
            first_name=user.get("first_name"),
            last_name=user.get("last_name"),
            active=str(user.get("active", "true")).lower() == "true",
        )

    # ============================================================
    # Find Approval Request by Sys ID
    # ============================================================

    def find_by_sys_id(
        self,
        sys_id: str,
    ) -> ApprovalRequest | None:
        """
        Retrieve an approval request by sys_id.

        Placeholder for future implementation.
        """

        raise NotImplementedError

    # ============================================================
    # Map Create Response
    # ============================================================

    def _map_create_response(
        self,
        data: dict,
    ) -> ApprovalRequestCreateResponse:
        """
        Convert a ServiceNow create response into an
        ApprovalRequestCreateResponse model.
        """

        return ApprovalRequestCreateResponse(
            sys_id=data["sys_id"],
            number=data["number"],
        )

    # ============================================================
    # Map Approval Request
    # ============================================================

    def _map_approval(
        self,
        data: dict,
    ) -> ApprovalRequest:
        """
        Convert a ServiceNow approval record into
        an ApprovalRequest model.
        """

        return ApprovalRequest(
            sys_id=data["sys_id"],
            number=data["number"],
            approval_status=data["approval_status"],
            callback_status=data["callback_status"],
            user_creation_status=data["user_creation_status"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            username=data["username"],
            email=data["email"],
            fastapi_user_id=data["fastapi_user_id"],
            access_justification=data.get("access_justification"),
            approved_at=data.get("approved_at"),
            rejected_at=data.get("rejected_at"),
            rejection_reason=data.get("rejection_reason"),
        )
