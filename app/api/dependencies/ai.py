"""
AI Dependencies

Purpose:
- Provide a shared AI orchestrator.
"""

from app.application.ai.orchestrator import AIOrchestrator
from app.infrastructure.ai.base import AIProvider
from app.infrastructure.ai.providers.gemini import GeminiProvider
from app.infrastructure.ai.providers.ollama import OllamaProvider
from app.infrastructure.ai.providers.rule_engine import RuleEngineProvider

# ============================================================
# Shared Orchestrator
# ============================================================

_ai_provider = AIOrchestrator(
    providers=[
        GeminiProvider(),
        OllamaProvider(),
        RuleEngineProvider(),
    ],
)

# ============================================================
# Dependency
# ============================================================


def get_ai_provider_dependency() -> AIProvider:
    """
    Return the shared AI provider.
    """

    return _ai_provider
