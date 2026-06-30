"""
Health Response Schema

Purpose:
- Define the response model for health endpoints.
"""

from pydantic import BaseModel

# ============================================================
# Health Response
# ============================================================


class HealthResponse(BaseModel):
    """
    Response returned by the health endpoint.
    """

    status: str

    application: str

    version: str
