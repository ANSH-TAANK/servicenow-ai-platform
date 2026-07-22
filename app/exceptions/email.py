"""
Email Exceptions

Purpose:
- Define email-related exceptions used
  across the infrastructure layer.
"""


class EmailProviderError(Exception):
    """
    Raised when an email provider
    fails to send an email.
    """

    pass
