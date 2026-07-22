"""
Email Service

Purpose:
- Coordinate email rendering and delivery.
- Orchestrate the email infrastructure.
- Provide business-oriented email operations.
"""

# Local Imports
from app.infrastructure.email.base import EmailProvider
from app.infrastructure.email.models import EmailMessage, EmailSendResult
from app.infrastructure.email.renderer import EmailTemplateRenderer

# ============================================================
# Email Service
# ============================================================


class EmailService:
    """
    Coordinate email rendering and delivery.
    """

    def __init__(
        self,
        provider: EmailProvider,
        renderer: EmailTemplateRenderer,
    ) -> None:
        """
        Initialize the email service.
        """

        self._provider = provider
        self._renderer = renderer

    # ============================================================
    # Send Email
    # ============================================================

    async def send_email(
        self,
        message: EmailMessage,
    ) -> EmailSendResult:
        """
        Render and send an email.
        """

        # --------------------------------------------------------
        # Render HTML
        # --------------------------------------------------------

        html = self._renderer.render(
            template=message.template,
            title=message.subject,
            context=message.context,
        )

        # --------------------------------------------------------
        # Generate Plain Text
        # --------------------------------------------------------

        text = "Please use an HTML compatible " "email client to view this email."

        # --------------------------------------------------------
        # Send Email
        # --------------------------------------------------------

        return await self._provider.send_email(
            to_email=message.to_email,
            subject=message.subject,
            html=html,
            text=text,
        )
