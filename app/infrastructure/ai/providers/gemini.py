"""
Gemini AI Provider

Purpose:
- Implement the AIProvider interface
  using Google's official GenAI SDK.
"""

from google import genai

from app.core.config import settings
from app.core.logging import get_logger
from app.exceptions.ai import GeminiAPIError
from app.infrastructure.ai.base import AIProvider
from app.infrastructure.ai.enums import AIProviderType
from app.infrastructure.ai.models import AIProviderRequest, AIProviderResponse
from app.infrastructure.ai.prompts import build_incident_prompt
from app.infrastructure.ai.providers.utils import parse_ai_response

logger = get_logger(__name__)


# ============================================================
# Gemini Provider
# ============================================================


class GeminiProvider(AIProvider):
    """
    Google Gemini implementation
    of AIProvider.
    """

    def __init__(self) -> None:
        """
        Initialize Gemini provider.
        """

        logger.info("Initializing Gemini provider.")

        self._model_name = settings.ai.gemini_model

        self._client = genai.Client(
            api_key=settings.ai.gemini_api_key,
        )

        logger.info(
            "Gemini provider initialized using model '%s'.",
            self._model_name,
        )

    # ============================================================
    # Prediction
    # ============================================================

    def predict(
        self,
        request: AIProviderRequest,
    ) -> AIProviderResponse:
        """
        Predict incident fields.
        """

        logger.info("Generating prediction using Gemini.")

        prompt = build_incident_prompt(
            request.issue,
        )

        try:

            response = self._client.models.generate_content(
                model=self._model_name,
                contents=prompt,
            )

        except Exception as exc:

            logger.warning(
                "Gemini request failed: %s",
                exc,
            )

            raise GeminiAPIError() from exc

        # --------------------------------------------------------
        # Defensive check
        # --------------------------------------------------------

        text = response.text

        if text is None:

            raise GeminiAPIError(
                "Gemini returned an empty response.",
            )

        return parse_ai_response(
            text=text,
            provider=AIProviderType.GEMINI,
            model=self._model_name,
        )
