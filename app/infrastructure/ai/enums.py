"""
AI Enums

Purpose:
- Define enumerations used throughout
  the AI infrastructure.
"""

from enum import Enum

# ============================================================
# AI Provider
# ============================================================


class AIProviderType(str, Enum):
    """
    Supported AI providers.
    """

    GEMINI = "gemini"

    OLLAMA = "ollama"

    RULE_ENGINE = "rule_engine"


# ============================================================
# Impact
# ============================================================


class ImpactLevel(str, Enum):
    """
    ServiceNow impact levels.

    1 = High
    2 = Medium
    3 = Low
    """

    HIGH = "1"

    MEDIUM = "2"

    LOW = "3"


# ============================================================
# Urgency
# ============================================================


class UrgencyLevel(str, Enum):
    """
    ServiceNow urgency levels.

    1 = High
    2 = Medium
    3 = Low
    """

    HIGH = "1"

    MEDIUM = "2"

    LOW = "3"
