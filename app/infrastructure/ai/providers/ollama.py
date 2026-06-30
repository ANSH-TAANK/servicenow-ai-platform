"""
Ollama AI Provider

Purpose:
- Implement the AIProvider interface
  using Ollama.
"""

import httpx

from app.core.config import settings
from app.core.logging import get_logger
from app.exceptions.ai import OllamaAPIError
from app.infrastructure.ai.base import AIProvider
from app.infrastructure.ai.enums import AIProviderType
from app.infrastructure.ai.models import AIProviderRequest, AIProviderResponse
from app.infrastructure.ai.prompts import build_incident_prompt
from app.infrastructure.ai.providers.utils import parse_ai_response

logger = get_logger(__name__)


# ============================================================
# Ollama Provider
# ============================================================


class OllamaProvider(AIProvider):
    """
    Ollama implementation of AIProvider.
    """

    def __init__(self) -> None:
        """
        Initialize Ollama provider.
        """

        logger.info("Initializing Ollama provider.")

        self._base_url = settings.ai.ollama_base_url
        self._model_name = settings.ai.ollama_model

        self._client = httpx.Client(
            timeout=60,
        )

        logger.info(
            "Ollama provider initialized using model '%s'.",
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

        logger.info("Generating prediction using Ollama.")

        prompt = build_incident_prompt(
            request.issue,
        )

        try:

            response = self._client.post(
                f"{self._base_url}/api/generate",
                json={
                    "model": self._model_name,
                    "prompt": prompt,
                    "stream": False,
                },
            )

            response.raise_for_status()

        except Exception as exc:

            logger.warning(
                "Ollama request failed: %s",
                exc,
            )

            raise OllamaAPIError() from exc

        text = response.json()["response"]

        return parse_ai_response(
            text=text,
            provider=AIProviderType.OLLAMA,
            model=self._model_name,
        )
