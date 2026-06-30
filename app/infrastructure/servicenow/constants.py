"""
ServiceNow Constants

Purpose:
- Store constants used by the ServiceNow client.
- Avoid magic strings throughout the codebase.
"""

# ============================================================
# HTTP
# ============================================================

DEFAULT_TIMEOUT = 30

# ============================================================
# Content Types
# ============================================================

APPLICATION_JSON = "application/json"

# ============================================================
# HTTP Headers
# ============================================================

DEFAULT_HEADERS = {
    "Accept": APPLICATION_JSON,
    "Content-Type": APPLICATION_JSON,
}

# ============================================================
# Success Status Codes
# ============================================================

HTTP_OK = 200

HTTP_CREATED = 201

HTTP_NO_CONTENT = 204

# ============================================================
# HTTP Methods
# ============================================================

HTTP_GET = "GET"

HTTP_POST = "POST"

HTTP_PUT = "PUT"

HTTP_PATCH = "PATCH"

HTTP_DELETE = "DELETE"
