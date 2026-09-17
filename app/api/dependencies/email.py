"""
Email Dependencies

Purpose:
- Provide email-related dependencies.
- Construct email services.
- Support dependency injection for email delivery.
"""

from app.core.config import settings
from app.infrastructure.email.providers.resend import ResendEmailProvider
from app.infrastructure.email.renderer import EmailTemplateRenderer
from app.infrastructure.email.service import EmailService


def get_email_service() -> EmailService:
    """
    Provide the configured email service.
    """

    if settings.email.provider.lower() != "resend":
        raise ValueError(f"Unsupported email provider: {settings.email.provider}")

    provider = ResendEmailProvider()
    renderer = EmailTemplateRenderer()

    return EmailService(
        provider=provider,
        renderer=renderer,
    )
