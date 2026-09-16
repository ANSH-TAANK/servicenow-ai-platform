"""
Webhook Dependencies

Purpose:
- Provide webhook authentication dependencies.
- Construct webhook security services.

This module DOES NOT:
- Contain business logic.
- Validate requests directly.
"""

from app.core.webhook import WebhookSecurity

# ============================================================
# Webhook Security Dependency
# ============================================================


def get_webhook_security() -> WebhookSecurity:
    """
    Provide a webhook security instance.
    """

    return WebhookSecurity()
