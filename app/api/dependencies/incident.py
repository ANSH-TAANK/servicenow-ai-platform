"""
Incident Dependencies

Purpose:

- Provide IncidentService instances.
- Provide incident access control dependencies.
"""

from uuid import UUID

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.ai import get_ai_provider_dependency
from app.api.dependencies.auth import get_current_user_id
from app.api.dependencies.email import get_email_service
from app.api.dependencies.servicenow import get_servicenow_client
from app.application.approval.service import ApprovalService
from app.application.incident.service import IncidentService
from app.infrastructure.database.models.user import User
from app.infrastructure.database.repositories.user import UserRepository
from app.infrastructure.database.session import get_db
from app.infrastructure.email.service import EmailService

# ============================================================
# Incident Access Dependency
# ============================================================


async def require_incident_access(
    user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Ensure the authenticated user is allowed
    to create ServiceNow incidents.

    Returns:
        The authenticated and authorized platform user.
    """

    users = UserRepository(db)

    user = await users.get_by_id(
        user_id,
    )

    # --------------------------------------------------------
    # User Check
    # --------------------------------------------------------

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account not found.",
        )

    # --------------------------------------------------------
    # Email Verification Check
    # --------------------------------------------------------

    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email verification is required.",
        )

    # --------------------------------------------------------
    # ServiceNow Identity Check
    # --------------------------------------------------------

    if not user.is_servicenow_user or not user.servicenow_sys_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ServiceNow user access is not approved.",
        )

    # --------------------------------------------------------
    # Approval Check
    # --------------------------------------------------------

    approval_service = ApprovalService(
        db,
    )

    if not await approval_service.can_user_login(
        user_id,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User access has not been approved.",
        )

    return user


# ============================================================
# Incident Service Dependency
# ============================================================


def get_incident_service(
    email_service: EmailService = Depends(
        get_email_service,
    ),
) -> IncidentService:
    """
    Return an IncidentService instance.
    """

    provider = get_ai_provider_dependency()

    servicenow = get_servicenow_client()

    return IncidentService(
        provider=provider,
        servicenow=servicenow,
        email_service=email_service,
    )
