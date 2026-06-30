"""
AI Models

Purpose:
- Define request and response models used
  by AI providers.
"""

from pydantic import BaseModel

from app.infrastructure.ai.enums import AIProviderType, ImpactLevel, UrgencyLevel

# ============================================================
# AI Provider Request
# ============================================================


class AIProviderRequest(BaseModel):
    """
    Request sent to an AI provider.
    """

    issue: str


# ============================================================
# Incident Prediction
# ============================================================


class IncidentPrediction(BaseModel):
    """
    AI prediction for a ServiceNow incident.
    """

    short_description: str

    description: str  # ⭐ Add this

    category: str

    subcategory: str

    impact: ImpactLevel

    urgency: UrgencyLevel

    assignment_group: str

    confidence: float


# ============================================================
# AI Provider Response
# ============================================================


class AIProviderResponse(BaseModel):
    """
    Standard response returned
    by every AI provider.
    """

    prediction: IncidentPrediction

    provider: AIProviderType

    model: str
