"""
Rule Engine Provider

Purpose:
- Deterministic incident prediction.
- Final fallback when all AI providers fail.
"""

from app.infrastructure.ai.base import AIProvider
from app.infrastructure.ai.enums import AIProviderType, ImpactLevel, UrgencyLevel
from app.infrastructure.ai.models import (
    AIProviderRequest,
    AIProviderResponse,
    IncidentPrediction,
)

# ============================================================
# Rule Engine Provider
# ============================================================


class RuleEngineProvider(AIProvider):
    """
    Deterministic rule-based provider.

    Used as the final fallback if
    Gemini and Ollama are unavailable.
    """

    # ========================================================
    # Helpers
    # ========================================================

    def _build_response(
        self,
        prediction: IncidentPrediction,
    ) -> AIProviderResponse:

        return AIProviderResponse(
            prediction=prediction,
            provider=AIProviderType.RULE_ENGINE,
            model="rule-engine",
        )

    # ========================================================
    # Individual Rules
    # ========================================================

    def _vpn_rule(
        self,
        text: str,
        issue: str,
    ) -> AIProviderResponse | None:

        if "vpn" not in text:
            return None

        prediction = IncidentPrediction(
            short_description="VPN Connection Failure",
            description=issue,
            category="Network",
            subcategory="VPN",
            impact=ImpactLevel.MEDIUM,
            urgency=UrgencyLevel.MEDIUM,
            assignment_group="Network Team",
            confidence=0.60,
        )

        return self._build_response(prediction)

    def _password_rule(
        self,
        text: str,
        issue: str,
    ) -> AIProviderResponse | None:

        if "password" not in text and "login" not in text:
            return None

        prediction = IncidentPrediction(
            short_description="User Access Issue",
            description=issue,
            category="Access",
            subcategory="Password Reset",
            impact=ImpactLevel.LOW,
            urgency=UrgencyLevel.MEDIUM,
            assignment_group="Service Desk",
            confidence=0.60,
        )

        return self._build_response(prediction)

    def _printer_rule(
        self,
        text: str,
        issue: str,
    ) -> AIProviderResponse | None:

        if "printer" not in text:
            return None

        prediction = IncidentPrediction(
            short_description="Printer Malfunction",
            description=issue,
            category="Hardware",
            subcategory="Printer",
            impact=ImpactLevel.LOW,
            urgency=UrgencyLevel.LOW,
            assignment_group="Desktop Support",
            confidence=0.60,
        )

        return self._build_response(prediction)

    def _generic_rule(
        self,
        issue: str,
    ) -> AIProviderResponse:

        prediction = IncidentPrediction(
            short_description="General IT Issue",
            description=issue,
            category="General",
            subcategory="Other",
            impact=ImpactLevel.LOW,
            urgency=UrgencyLevel.LOW,
            assignment_group="Service Desk",
            confidence=0.50,
        )

        return self._build_response(prediction)

    # ========================================================
    # Public API
    # ========================================================

    def predict(
        self,
        request: AIProviderRequest,
    ) -> AIProviderResponse:
        """
        Predict incident fields using
        deterministic business rules.
        """

        issue = request.issue
        text = issue.lower()

        rules = (
            self._vpn_rule,
            self._password_rule,
            self._printer_rule,
        )

        for rule in rules:

            result = rule(
                text=text,
                issue=issue,
            )

            if result is not None:
                return result

        return self._generic_rule(
            issue,
        )
