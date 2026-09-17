"""
Authentication Dependencies

Purpose:
- Provide authentication-related dependencies.
- Construct authentication services.
- Support dependency injection for authentication.

This module DOES NOT:
- Authenticate users.
- Decode JWT tokens.
- Access HTTP requests directly.
"""

from uuid import UUID

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.email import get_email_service
from app.application.auth.service import AuthenticationService
from app.core.constants import JWT_SUBJECT
from app.core.security import decode_access_token
from app.infrastructure.database.session import get_db
from app.infrastructure.email.service import EmailService

# ============================================================
# OAuth2 Bearer Scheme
# ============================================================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/token",
)

# ============================================================
# Authentication Service Dependency
# ============================================================


async def get_auth_service(
    db: AsyncSession = Depends(get_db),
    email_service: EmailService = Depends(get_email_service),
) -> AuthenticationService:
    """
    Provide an authentication service.
    """

    return AuthenticationService(
        db=db,
        email_service=email_service,
    )


# ============================================================
# Current User ID Dependency
# ============================================================


async def get_current_user_id(
    token: str = Depends(
        oauth2_scheme,
    ),
) -> UUID:
    """
    Extract the authenticated user's ID from an access token.
    """

    payload = decode_access_token(
        token,
    )

    return UUID(
        payload[JWT_SUBJECT],
    )
