"""
Application Constants

Purpose:
- Store application-wide constant values.
- Avoid magic numbers and hardcoded strings.
- Improve maintainability.

This module SHOULD NOT contain:
- Environment variables
- Business logic
- Configuration
"""

# ============================================================
# Database Field Lengths
# ============================================================

SERVICENOW_SYS_ID_LENGTH = 32

USERNAME_MAX_LENGTH = 100

NAME_MAX_LENGTH = 255

EMAIL_MAX_LENGTH = 255

# ============================================================
# ServiceNow Connection
# ============================================================

INSTANCE_URL_MAX_LENGTH = 255

INSTANCE_NAME_MAX_LENGTH = 100

SERVICENOW_USERNAME_MAX_LENGTH = 100

ENCRYPTED_CREDENTIAL_MAX_LENGTH = 1024

# ============================================================
# Database Tables
# ============================================================

TABLE_USERS = "users"

TABLE_SERVICENOW_CONNECTIONS = "servicenow_connections"

TABLE_CONVERSATIONS = "conversations"

TABLE_INCIDENTS = "incidents"

TABLE_USER_PREFERENCES = "user_preferences"


# ============================================================
# Password Policy
# ============================================================
PASSWORD_HASH_MAX_LENGTH = 255

PASSWORD_MIN_LENGTH = 8

PASSWORD_MAX_LENGTH = 128

# ============================================================
# JWT
# ============================================================

ACCESS_TOKEN_TYPE = "access"

REFRESH_TOKEN_TYPE = "refresh"

JWT_SUBJECT = "sub"

JWT_TYPE = "type"

JWT_JTI = "jti"

JWT_IAT = "iat"

JWT_EXP = "exp"


# ============================================================
# Validation Patterns
# ============================================================

USERNAME_PATTERN = r"^[A-Za-z0-9_]+$"

PASSWORD_UPPERCASE_PATTERN = r"[A-Z]"

PASSWORD_LOWERCASE_PATTERN = r"[a-z]"

PASSWORD_DIGIT_PATTERN = r"\d"

PASSWORD_SPECIAL_CHARACTER_PATTERN = r"[!@#$%^&*(),.?\":{}|<>]"

# ============================================================
# Reserved Usernames
# ============================================================

RESERVED_USERNAMES = {
    "admin",
    "administrator",
    "root",
    "system",
    "support",
    "servicenow",
    "api",
    "ai",
    "backend",
    "test",
}


# ============================================================
# HTTP Authentication
# ============================================================

BEARER_TOKEN_TYPE = "Bearer"


# ============================================================
# Error Codes
# ============================================================

APPLICATION_ERROR = "APPLICATION_ERROR"

AUTHENTICATION_ERROR = "AUTHENTICATION_ERROR"

USER_ALREADY_EXISTS_ERROR = "USER_ALREADY_EXISTS"

USER_NOT_FOUND_ERROR = "USER_NOT_FOUND"

INVALID_CREDENTIALS_ERROR = "INVALID_CREDENTIALS"

USER_INACTIVE_ERROR = "USER_INACTIVE"

INVALID_PASSWORD_ERROR = "INVALID_PASSWORD"

INVALID_USERNAME_ERROR = "INVALID_USERNAME"

EMAIL_ALREADY_EXISTS_ERROR = "EMAIL_ALREADY_EXISTS"

USERNAME_ALREADY_EXISTS_ERROR = "USERNAME_ALREADY_EXISTS"

VERIFICATION_CODE_NOT_FOUND_ERROR = "verification_code_not_found"

VERIFICATION_CODE_EXPIRED_ERROR = "verification_code_expired"

VERIFICATION_CODE_INVALID_ERROR = "verification_code_invalid"

VERIFICATION_ATTEMPTS_EXCEEDED_ERROR = "verification_attempts_exceeded"

VERIFICATION_RESEND_LIMIT_EXCEEDED_ERROR = "verification_resend_limit_exceeded"

VERIFICATION_RESEND_TOO_SOON_ERROR = "verification_resend_too_soon"

VERIFICATION_ALREADY_COMPLETED_ERROR = "verification_already_completed"

# ============================================================
# Verification
# ============================================================

TABLE_VERIFICATION_CODES = "verification_codes"

OTP_HASH_MAX_LENGTH = 255

VERIFICATION_PURPOSE_MAX_LENGTH = 50

OTP_LENGTH = 6

OTP_EXPIRY_MINUTES = 10

MAX_OTP_VERIFICATION_ATTEMPTS = 5

MAX_OTP_RESEND_ATTEMPTS = 3

OTP_RESEND_COOLDOWN_SECONDS = 60

VERIFICATION_CODE_EXPIRATION_MINUTES = 10

AUTH_USER_NOT_VERIFIED = "AUTH_USER_NOT_VERIFIED"


# ============================================================
# User Approval
# ============================================================

TABLE_USER_APPROVALS = "user_approvals"

APPROVAL_REASON_MAX_LENGTH = 500
APPROVED_BY_MAX_LENGTH = 255


USER_APPROVAL_PENDING_ERROR = "USER_APPROVAL_PENDING_ERROR"
