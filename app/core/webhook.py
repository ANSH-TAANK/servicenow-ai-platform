"""
Webhook Security

Purpose:
- Generate and verify HMAC webhook signatures.
- Protect incoming webhook requests.
- Prevent replay attacks.

This module DOES NOT:
- Access the database.
- Contain business logic.
- Depend on FastAPI.
"""

import hashlib
import hmac
import time

from app.core.config import settings
from app.core.constants import WEBHOOK_TIMESTAMP_TOLERANCE_SECONDS


class WebhookSecurity:
    """
    Handles webhook authentication.
    """

    def generate_signature(
        self,
        timestamp: str,
        body: str,
    ) -> str:
        """
        Generate an HMAC SHA-256 signature.
        """

        message = f"{timestamp}.{body}"

        return hmac.new(
            settings.webhook.secret.encode(),
            message.encode(),
            hashlib.sha256,
        ).hexdigest()

    def verify_signature(
        self,
        received_signature: str | None,
        timestamp: str,
        body: str,
    ) -> bool:
        """
        Verify the received HMAC signature.
        """

        if not received_signature:
            return False

        expected_signature = self.generate_signature(
            timestamp,
            body,
        )

        return hmac.compare_digest(
            received_signature,
            expected_signature,
        )

    def verify_timestamp(
        self,
        timestamp: str | None,
    ) -> bool:
        """
        Verify the webhook timestamp to prevent replay attacks.
        """

        if not timestamp:
            return False

        try:
            request_timestamp = int(timestamp)

        except (TypeError, ValueError):
            return False

        current_timestamp = int(time.time())

        return (
            abs(current_timestamp - request_timestamp)
            <= WEBHOOK_TIMESTAMP_TOLERANCE_SECONDS
        )
