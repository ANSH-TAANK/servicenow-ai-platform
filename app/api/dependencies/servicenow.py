"""
ServiceNow Dependencies

Purpose:
- Provide shared ServiceNow client instances.
"""

from app.infrastructure.servicenow.client import ServiceNowClient

# ============================================================
# Shared Client
# ============================================================

_servicenow_client = ServiceNowClient()


# ============================================================
# Dependency
# ============================================================


def get_servicenow_client() -> ServiceNowClient:
    """
    Return the shared ServiceNow client.
    """

    return _servicenow_client
