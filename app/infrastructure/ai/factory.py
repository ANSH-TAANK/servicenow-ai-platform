"""
AI Provider Factory

Purpose:
- Build AI providers.
"""

from app.core.config import settings
from app.core.logging import get_logger
from app.exceptions.ai import AIProviderConfigurationError
from app.infrastructure.ai.base import AIProvider
from app.infrastructure.ai.enums import AIProviderType
from app.infrastructure.ai.providers.gemini import GeminiProvider
from app.infrastructure.ai.providers.ollama import OllamaProvider

logger = get_logger(__name__)


# ============================================================
# Provider Registry
# ============================================================

_PROVIDER_REGISTRY = {
    AIProviderType.GEMINI.value: GeminiProvider,
    AIProviderType.OLLAMA.value: OllamaProvider,
}


# ============================================================
# Single Provider
# ============================================================


def get_ai_provider() -> AIProvider:
    """
    Return the configured provider.
    """

    provider_name = settings.ai.default_provider.lower()

    logger.info(
        "Selected AI provider: %s",
        provider_name,
    )

    provider_cls = _PROVIDER_REGISTRY.get(provider_name)

    if provider_cls is None:
        raise AIProviderConfigurationError(
            f"Unsupported AI provider '{provider_name}'."
        )

    return provider_cls()


# ============================================================
# Available Providers
# ============================================================


def get_available_providers() -> list[AIProvider]:
    """
    Return all configured providers
    in priority order.

    Priority:
    1. Gemini
    2. Ollama
    """

    return [
        GeminiProvider(),
        OllamaProvider(),
    ]
