"""
AI Orchestrator

Purpose:
- Coordinate multiple AI providers.
- Provide automatic failover.
"""

from app.core.logging import get_logger
from app.infrastructure.ai.base import AIProvider
from app.infrastructure.ai.models import AIProviderRequest, AIProviderResponse

logger = get_logger(__name__)


# ============================================================
# AI Orchestrator
# ============================================================


class AIOrchestrator(AIProvider):
    """
    Try AI providers in order until
    one succeeds.
    """

    def __init__(
        self,
        providers: list[AIProvider],
    ) -> None:

        self._providers = providers

    # ========================================================
    # Prediction
    # ========================================================

    def predict(
        self,
        request: AIProviderRequest,
    ) -> AIProviderResponse:
        """
        Try each provider until one
        successfully returns a prediction.
        """

        last_exception: Exception | None = None

        for provider in self._providers:

            provider_name = provider.__class__.__name__

            logger.info(
                "Trying AI provider: %s",
                provider_name,
            )

            try:

                response = provider.predict(request)

                logger.info(
                    "AI provider '%s' succeeded.",
                    provider_name,
                )

                return response

            except Exception as exc:

                last_exception = exc

                logger.warning(
                    "AI provider '%s' failed: %s",
                    provider_name,
                    str(exc),
                )

        logger.error("All AI providers failed.")

        if last_exception is not None:
            raise last_exception

        raise RuntimeError("No AI providers configured.")
