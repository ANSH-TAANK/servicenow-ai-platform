"""
Email Models

Purpose:
- Define internal email infrastructure models.
- Standardize email provider responses.
- Provide a common result model for all email providers.

This module DOES NOT:
- Send emails.
- Render email templates.
- Contain business logic.
"""

# Standard Library Imports
from dataclasses import dataclass

# ============================================================
# Email Send Result
# ============================================================


@dataclass(
    slots=True,
)
class EmailSendResult:
    """
    Represents the result of an email delivery attempt.

    Responsibilities
    ----------------
    - Store email delivery status.
    - Store provider metadata.
    - Standardize responses across providers.

    This class DOES NOT
    -------------------
    - Send emails.
    - Retry failed deliveries.
    - Perform validation.
    """

    success: bool
    provider: str
    message_id: str | None = None
    error: str | None = None


# ============================================================
# Email Message
# ============================================================


@dataclass(
    slots=True,
)
class EmailMessage:
    """
    Represents an email to be sent.

    Responsibilities
    ----------------
    - Store email metadata.
    - Store template information.
    - Store template context.

    This class DOES NOT
    -------------------
    - Render templates.
    - Send emails.
    - Generate email content.
    """

    to_email: str

    subject: str

    template: str

    context: dict[str, str]
