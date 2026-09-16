"""
Webhook Authentication Dependency

Purpose:
- Authenticate incoming ServiceNow webhook requests.
- Validate the shared API key.
"""

import hmac

from fastapi import Header, HTTPException, status

from app.core.config import settings


async def verify_webhook(
    x_api_key: str | None = Header(
        default=None,
        alias="X-API-Key",
    ),
) -> None:
    """
    Verify incoming webhook API key.
    """

    if not x_api_key:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing webhook API key.",
        )

    if not hmac.compare_digest(
        x_api_key,
        settings.webhook.api_key,
    ):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid webhook API key.",
        )
