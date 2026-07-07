"""
Security Exceptions

Purpose:
- Define security-related exceptions.
- Decouple the application from third-party JWT libraries.

This module DOES NOT:
- Create JWT tokens.
- Verify passwords.
- Access the database.
"""

# ============================================================
# Base Security Exception
# ============================================================


class SecurityError(Exception):
    """
    Base class for all security-related exceptions.
    """


# ============================================================
# Invalid Token
# ============================================================


class InvalidTokenError(SecurityError):
    """
    Raised when a JWT token is invalid.
    """


# ============================================================
# Expired Token
# ============================================================


class ExpiredTokenError(SecurityError):
    """
    Raised when a JWT token has expired.
    """


# ============================================================
# Invalid Token Type
# ============================================================


class InvalidTokenTypeError(SecurityError):
    """
    Raised when a JWT token type is invalid.
    """
