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

from pydantic import BaseModel, computed_field
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
# Database Configuration
# ============================================================


class DatabaseSettings(ConfigModel):
    """Database configuration."""

    host: str
    port: int
    name: str
    username: str
    password: str

    echo: bool

    pool_size: int
    max_overflow: int
    pool_timeout: int
    pool_recycle: int

    @computed_field
    @property
    def url(self) -> str:
        """
        SQLAlchemy database connection URL.

        Example:
        postgresql+psycopg://postgres:password@localhost:5432/postgres
        """

        return (
            f"postgresql+psycopg://"
            f"{self.username}:"
            f"{self.password}@"
            f"{self.host}:"
            f"{self.port}/"
            f"{self.name}"
        )


# ============================================================
# Security Configuration
# ============================================================


class SecuritySettings(ConfigModel):
    """Security configuration."""

    access_token_secret: str

    refresh_token_secret: str

    jwt_algorithm: str

    access_token_expire_minutes: int

    refresh_token_expire_days: int


# ============================================================
# Email Configuration
# ============================================================


class EmailSettings(ConfigModel):
    """Email provider configuration."""

    provider: str

    resend_api_key: str

    from_name: str

    from_email: str


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
    database: DatabaseSettings
    security: SecuritySettings
    email: EmailSettings

    model_config = SettingsConfigDict(
        frozen=True,
        extra="ignore",
    )
