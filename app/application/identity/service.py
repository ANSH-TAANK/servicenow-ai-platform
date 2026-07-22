"""
Identity Service

Purpose:
- Coordinate platform user identity verification.
- Synchronize platform users with ServiceNow.
- Encapsulate identity business logic.
"""

from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.application.identity.exceptions import PlatformUserNotFoundError
from app.application.identity.responses import VerifyIdentityResponse
from app.core.logging import get_logger
from app.domain.enums.identity import IdentityStatus
from app.infrastructure.database.models.user import User
from app.infrastructure.database.repositories.user import UserRepository
from app.infrastructure.servicenow.models import ServiceNowUser
from app.infrastructure.servicenow.user_service import ServiceNowUserService

logger = get_logger(__name__)


# ============================================================
# Identity Service
# ============================================================


class IdentityService:
    """
    Coordinates ServiceNow identity verification
    for platform users.
    """

    # ============================================================
    # Constructor
    # ============================================================

    def __init__(
        self,
        db: AsyncSession,
        users: UserRepository,
        servicenow_users: ServiceNowUserService,
    ) -> None:
        """
        Initialize the identity service.
        """

        self._db = db
        self._users = users
        self._servicenow_users = servicenow_users

    # ============================================================
    # Verify Identity
    # ============================================================

    async def verify_identity(
        self,
        user_id: UUID,
    ) -> VerifyIdentityResponse:
        """
        Verify whether a platform user exists
        in ServiceNow.
        """

        logger.info(
            "Verifying ServiceNow identity for platform user %s.",
            user_id,
        )

        user = await self._users.get_by_id(
            user_id,
        )

        if user is None:
            logger.warning(
                "Platform user %s not found.",
                user_id,
            )

            raise PlatformUserNotFoundError(
                "Platform user not found.",
            )

        servicenow_user = self._servicenow_users.find_by_email(
            user.email,
        )

        if servicenow_user is None:
            logger.info(
                "Platform user '%s' does not exist in ServiceNow.",
                user.email,
            )

            return VerifyIdentityResponse(
                user_id=user.id,
                status=IdentityStatus.NOT_LINKED,
                message="User does not exist in ServiceNow.",
            )

        logger.info(
            "Platform user '%s' linked with ServiceNow user '%s'.",
            user.email,
            servicenow_user.sys_id,
        )

        self._update_identity(
            user,
            servicenow_user,
        )

        await self._users.update(
            user,
        )

        await self._db.commit()

        return VerifyIdentityResponse(
            user_id=user.id,
            status=IdentityStatus.LINKED,
            servicenow_sys_id=servicenow_user.sys_id,
            servicenow_username=servicenow_user.username,
            servicenow_email=servicenow_user.email,
            message="ServiceNow identity verified successfully.",
        )

    # ============================================================
    # Private Helpers
    # ============================================================

    def _update_identity(
        self,
        user: User,
        servicenow_user: ServiceNowUser,
    ) -> None:
        """
        Update the local platform user's
        ServiceNow identity mapping.
        """

        if user.servicenow_sys_id != servicenow_user.sys_id:
            user.servicenow_sys_id = servicenow_user.sys_id

        if user.servicenow_username != servicenow_user.username:
            user.servicenow_username = servicenow_user.username

        if not user.is_servicenow_user:
            user.is_servicenow_user = True

        user.last_synced_at = datetime.now(
            UTC,
        )
