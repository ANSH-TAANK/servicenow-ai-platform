"""
Application Settings

Purpose:
- Define all configuration models.
- Group configuration into logical sections.
- Provide the root Settings model.

NOTE:
This file DOES NOT load environment variables.
Environment loading is handled by app/core/config.py.
"""

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

# ============================================================
# Base Configuration Model
# ============================================================


class ConfigModel(BaseModel):
    """
    Base configuration model.

    All configuration models inherit from this class.
    """

    model_config = {"frozen": True}


# ============================================================
# Application Configuration
# ============================================================


class ApplicationSettings(ConfigModel):
    """Application configuration."""

    name: str
    version: str
    environment: str
    debug: bool


# ============================================================
# AI Configuration
# ============================================================


class AISettings(ConfigModel):
    """AI provider configuration."""

    default_provider: str

    gemini_api_key: str

    gemini_model: str

    ollama_base_url: str

    ollama_model: str


# ============================================================
# ServiceNow Configuration
# ============================================================


class ServiceNowSettings(ConfigModel):
    """ServiceNow configuration."""

    url: str
    username: str
    password: str
    table: str


# ============================================================
# API Configuration
# ============================================================


class APISettings(ConfigModel):
    """API configuration."""

    prefix: str


# ============================================================
# Logging Configuration
# ============================================================


class LoggingSettings(ConfigModel):
    """Logging configuration."""

    level: str


# ============================================================
# HTTP Configuration
# ============================================================


class HTTPSettings(ConfigModel):
    """HTTP client configuration."""

    timeout: int


# ============================================================
# Root Settings
# ============================================================


class Settings(BaseSettings):
    """
    Root application configuration.

    Holds all grouped configuration objects.
    """

    application: ApplicationSettings
    ai: AISettings
    servicenow: ServiceNowSettings
    api: APISettings
    logging: LoggingSettings
    http: HTTPSettings

    model_config = SettingsConfigDict(
        frozen=True,
        extra="ignore",
    )
