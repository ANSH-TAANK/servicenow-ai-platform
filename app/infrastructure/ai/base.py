"""
AI Provider Interface

Purpose:
- Define the contract that every AI provider
  must implement.
"""

# abc means abstract base class
from abc import ABC, abstractmethod

from app.infrastructure.ai.models import AIProviderRequest, AIProviderResponse

# ============================================================
# AI Provider
# ============================================================


class AIProvider(ABC):
    """
    Base interface for all AI providers.
    """

    @abstractmethod
    def predict(
        self,
        request: AIProviderRequest,
    ) -> AIProviderResponse:
        """
        Predict ServiceNow incident fields
        from a user issue description.
        """

        raise NotImplementedError
