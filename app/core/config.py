import os
from typing import Any, Callable

from dotenv import load_dotenv

from app.core.settings import (
    AISettings,
    APISettings,
    ApplicationSettings,
    DatabaseSettings,
    HTTPSettings,
    LoggingSettings,
    SecuritySettings,
    ServiceNowSettings,
    Settings,
)

# ============================================================
# Load Environment Variables
# ============================================================

ENV_FILE = os.getenv(
    "ENV_FILE",
    ".env",
)

load_dotenv(
    dotenv_path=ENV_FILE,
    override=True,
)

# ============================================================
# Environment Helper
# ============================================================


def get_env(
    key: str,
    default: Any = None,
    cast: Callable = str,
) -> Any:
    """
    Read an environment variable and optionally
    convert it to the required type.
    """

    value = os.getenv(key, default)

    if value is None:
        raise ValueError(f"Environment variable '{key}' is missing.")

    if cast is bool:
        return str(value).lower() == "true"

    return cast(value)


# ============================================================
# Settings Loader
# ============================================================


def _load_settings() -> Settings:
    """
    Build the application's Settings object
    from environment variables.
    """

    application = ApplicationSettings(
        name=get_env("APP_NAME"),
        version=get_env("APP_VERSION"),
        environment=get_env("APP_ENV"),
        debug=get_env(
            "DEBUG",
            cast=bool,
        ),
    )

    ai = AISettings(
        default_provider=get_env("DEFAULT_AI_PROVIDER"),
        gemini_api_key=get_env("GEMINI_API_KEY"),
        gemini_model=get_env("GEMINI_MODEL"),
        ollama_base_url=get_env("OLLAMA_BASE_URL"),
        ollama_model=get_env("OLLAMA_MODEL"),
    )

    servicenow = ServiceNowSettings(
        url=get_env("SERVICENOW_URL"),
        username=get_env("SERVICENOW_USERNAME"),
        password=get_env("SERVICENOW_PASSWORD"),
        table=get_env("SERVICENOW_TABLE"),
    )

    api = APISettings(
        prefix=get_env("API_V1_PREFIX"),
    )

    logging = LoggingSettings(
        level=get_env("LOG_LEVEL"),
    )

    http = HTTPSettings(
        timeout=get_env(
            "HTTP_TIMEOUT",
            cast=int,
        ),
    )

    database = DatabaseSettings(
        host=get_env("DB_HOST"),
        port=get_env(
            "DB_PORT",
            cast=int,
        ),
        name=get_env("DB_NAME"),
        username=get_env("DB_USERNAME"),
        password=get_env("DB_PASSWORD"),
        echo=get_env(
            "DB_ECHO",
            cast=bool,
        ),
        pool_size=get_env(
            "DB_POOL_SIZE",
            cast=int,
        ),
        max_overflow=get_env(
            "DB_MAX_OVERFLOW",
            cast=int,
        ),
        pool_timeout=get_env(
            "DB_POOL_TIMEOUT",
            cast=int,
        ),
        pool_recycle=get_env(
            "DB_POOL_RECYCLE",
            cast=int,
        ),
    )

    security = SecuritySettings(
        access_token_secret=get_env("ACCESS_TOKEN_SECRET"),
        refresh_token_secret=get_env("REFRESH_TOKEN_SECRET"),
        jwt_algorithm=get_env("JWT_ALGORITHM"),
        access_token_expire_minutes=get_env(
            "ACCESS_TOKEN_EXPIRE_MINUTES",
            cast=int,
        ),
        refresh_token_expire_days=get_env(
            "REFRESH_TOKEN_EXPIRE_DAYS",
            cast=int,
        ),
    )

    return Settings(
        application=application,
        ai=ai,
        servicenow=servicenow,
        api=api,
        logging=logging,
        http=http,
        database=database,
        security=security,
    )


# ============================================================
# Singleton Settings Instance
# ============================================================

settings = _load_settings()
