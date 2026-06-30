"""
AI Exceptions

Purpose:
- Define all AI related exceptions.
"""

from app.exceptions.base import BaseApplicationException

# ============================================================
# Base AI Exception
# ============================================================


class AIError(BaseApplicationException):
    """
    Base exception for all AI related errors.
    """

    def __init__(
        self,
        message: str = "AI operation failed.",
        *,
        error_code: str = "AI_ERROR",
        status_code: int = 500,
    ) -> None:

        super().__init__(
            message=message,
            error_code=error_code,
            status_code=status_code,
        )


# ============================================================
# AI Provider Error
# ============================================================


class AIProviderError(AIError):
    """
    Raised when an AI provider fails.
    """

    def __init__(
        self,
        message: str = "AI provider operation failed.",
    ) -> None:

        super().__init__(
            message=message,
            error_code="AI_PROVIDER_ERROR",
        )


# ============================================================
# Gemini API Error
# ============================================================


class GeminiAPIError(AIProviderError):
    """
    Raised when Gemini API request fails.
    """

    def __init__(
        self,
        message: str = "Gemini API request failed.",
    ) -> None:

        super().__init__(message)

        self.error_code = "GEMINI_API_ERROR"
        self.status_code = 502


# ============================================================
# Ollama API Error
# ============================================================


class OllamaAPIError(AIProviderError):
    """
    Raised when Ollama API request fails.
    """

    def __init__(
        self,
        message: str = "Ollama API request failed.",
    ) -> None:

        super().__init__(message)

        self.error_code = "OLLAMA_API_ERROR"
        self.status_code = 502


# ============================================================
# AI Response Parsing Error
# ============================================================


class AIResponseParsingError(AIProviderError):
    """
    Raised when AI response parsing fails.
    """

    def __init__(
        self,
        message: str = "Failed to parse AI response.",
    ) -> None:

        super().__init__(message)

        self.error_code = "AI_RESPONSE_PARSING_ERROR"


# ============================================================
# AI Validation Error
# ============================================================


class AIValidationError(AIProviderError):
    """
    Raised when AI returns invalid values.
    """

    def __init__(
        self,
        message: str = "AI response validation failed.",
    ) -> None:

        super().__init__(message)

        self.error_code = "AI_VALIDATION_ERROR"


# ============================================================
# AI Provider Unavailable
# ============================================================


class AIProviderUnavailableError(AIProviderError):
    """
    Raised when an AI provider is unavailable.
    """

    def __init__(
        self,
        message: str = "AI provider is unavailable.",
    ) -> None:

        super().__init__(message)

        self.error_code = "AI_PROVIDER_UNAVAILABLE"


# ============================================================
# AI Provider Configuration Error
# ============================================================


class AIProviderConfigurationError(AIProviderError):
    """
    Raised when AI provider configuration is invalid.
    """

    def __init__(
        self,
        message: str = "AI provider configuration is invalid.",
    ) -> None:

        super().__init__(message)

        self.error_code = "AI_PROVIDER_CONFIGURATION_ERROR"
