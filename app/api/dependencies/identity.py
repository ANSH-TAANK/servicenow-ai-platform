"""
Identity Dependencies

Purpose:
- Provide IdentityService instances.
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.servicenow import get_servicenow_client
from app.application.identity.service import IdentityService
from app.infrastructure.database.repositories.user import UserRepository
from app.infrastructure.database.session import get_db
from app.infrastructure.servicenow.user_service import ServiceNowUserService

# ============================================================
# ServiceNow User Service Dependency
# ============================================================


def get_servicenow_user_service() -> ServiceNowUserService:
    """
    Return a ServiceNowUserService instance.
    """

    client = get_servicenow_client()

    return ServiceNowUserService(
        client=client,
    )


# ============================================================
# Identity Service Dependency
# ============================================================


async def get_identity_service(
    db: AsyncSession = Depends(get_db),
) -> IdentityService:
    """
    Return an IdentityService instance.
    """

    users = UserRepository(
        db=db,
    )

    servicenow_users = get_servicenow_user_service()

    return IdentityService(
        db=db,
        users=users,
        servicenow_users=servicenow_users,
    )
