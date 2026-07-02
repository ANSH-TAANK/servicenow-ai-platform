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
