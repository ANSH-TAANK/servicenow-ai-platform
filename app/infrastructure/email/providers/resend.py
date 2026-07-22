"""
Resend Email Provider

Purpose:
- Send emails using the Resend API.
- Implement the EmailProvider interface.
"""

import asyncio

import resend

from app.core.config import settings
from app.exceptions.email import EmailProviderError
from app.infrastructure.email.base import EmailProvider
from app.infrastructure.email.models import EmailSendResult


class ResendEmailProvider(EmailProvider):
    """
    Email provider implementation
    using the Resend API.
    """

    def __init__(self) -> None:
        """
        Configure the Resend client.
        """

        resend.api_key = settings.email.resend_api_key

    async def send_email(
        self,
        *,
        to_email: str,
        subject: str,
        html: str,
        text: str,
    ) -> EmailSendResult:
        """
        Send an email using Resend.
        """

        # --------------------------------------------------------
        # Send Email
        # --------------------------------------------------------

        try:
            response = await asyncio.to_thread(
                resend.Emails.send,
                {
                    "from": (
                        f"{settings.email.from_name} " f"<{settings.email.from_email}>"
                    ),
                    "to": [to_email],
                    "subject": subject,
                    "html": html,
                    "text": text,
                },
            )

            return EmailSendResult(
                success=True,
                provider="resend",
                message_id=response.get("id"),
            )

        except Exception as exc:
            raise EmailProviderError("Failed to send email using Resend.") from exc
