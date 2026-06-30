"""
AI Provider Utilities

Purpose:
- Parse and validate AI provider responses.
"""

import json

from pydantic import ValidationError

from app.exceptions.ai import AIResponseParsingError
from app.infrastructure.ai.enums import AIProviderType
from app.infrastructure.ai.models import AIProviderResponse, IncidentPrediction

# ============================================================
# Parse AI Response
# ============================================================


def parse_ai_response(
    text: str,
    provider: AIProviderType,
    model: str,
) -> AIProviderResponse:
    """
    Parse a raw AI response into validated
    application models.
    """

    # --------------------------------------------------------
    # Remove Markdown code fences
    # --------------------------------------------------------

    cleaned_text = text.strip().replace("```json", "").replace("```", "").strip()

    # --------------------------------------------------------
    # Parse JSON
    # --------------------------------------------------------

    try:
        data = json.loads(cleaned_text)

    except json.JSONDecodeError as exc:
        raise AIResponseParsingError("AI returned invalid JSON.") from exc

    # --------------------------------------------------------
    # Normalize provider output
    # --------------------------------------------------------

    # Some models omit confidence
    data.setdefault(
        "confidence",
        0.50,
    )

    # Some models return integers instead of strings
    if "impact" in data:
        data["impact"] = str(
            data["impact"],
        )

    if "urgency" in data:
        data["urgency"] = str(
            data["urgency"],
        )

    if "confidence" in data:
        data["confidence"] = float(data["confidence"])

    # --------------------------------------------------------
    # Validate AI response
    # --------------------------------------------------------

    try:
        prediction = IncidentPrediction.model_validate(
            data,
        )

    except ValidationError as exc:
        raise AIResponseParsingError(
            "AI response does not match the expected schema."
        ) from exc

    # --------------------------------------------------------
    # Build provider response
    # --------------------------------------------------------

    return AIProviderResponse(
        prediction=prediction,
        provider=provider,
        model=model,
    )
