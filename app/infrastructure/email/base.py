"""
Email Provider Abstraction

Purpose:
- Define the contract for all email providers.
- Ensure the application remains provider-agnostic.
- Standardize email delivery across different providers.

This module DOES NOT:
- Send emails.
- Render email templates.
- Generate OTPs.
- Contain business logic.
"""

# Standard Library Imports
from abc import ABC, abstractmethod

# Local Imports
from app.infrastructure.email.models import EmailSendResult

# Third-Party Imports


# ============================================================
# Email Provider Contract
# ============================================================


class EmailProvider(
    ABC,
):
    """
    Base contract for all email providers.

    Responsibilities
    ----------------
    - Define the interface for sending emails.
    - Ensure all providers expose a consistent API.

    This class DOES NOT
    -------------------
    - Implement provider-specific logic.
    - Know about OTPs.
    - Know about verification workflows.
    """

    @abstractmethod
    async def send_email(
        self,
        *,
        to_email: str,
        subject: str,
        html: str,
        text: str,
    ) -> EmailSendResult:
        """
        Send an email.

        Args:
            to_email:
                Recipient email address.

            subject:
                Email subject.

            html:
                HTML email content.

            text:
                Plain-text fallback content.

        Returns:
            EmailSendResult containing the delivery result.

        Raises:
            NotImplementedError:
                If the provider does not implement this method.
        """
        raise NotImplementedError
