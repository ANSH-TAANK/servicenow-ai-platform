"""
Application Entry Point

Purpose:

- Create the FastAPI application.
- Configure the application.
- Register all application components.

This is the application's entry point.
"""

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.api.router import router as api_router
from app.core.config import settings
from app.core.lifespan import lifespan
from app.core.logging import configure_logging, get_logger
from app.exceptions.handlers import register_exception_handlers

logger = get_logger(__name__)


# ============================================================
# Application Factory
# ============================================================


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """

    configure_logging()

    logger.info("Creating FastAPI application.")

    app = FastAPI(
        title=settings.application.name,
        summary=(
            "Enterprise AI-powered ServiceNow platform for "
            "intelligent incident management and secure enterprise integration."
        ),
        description="""
## ServiceNow AI Platform

Enterprise backend platform combining **AI-powered incident processing**,
**ServiceNow integration**, and **secure enterprise identity management**.

### Version 1 — AI & ServiceNow Foundation

Version 1 established the core platform with:

- AI-powered incident processing
- Intelligent incident classification
- Google Gemini integration
- Ollama integration
- Rule Engine fallback
- Automatic AI provider failover
- ServiceNow REST API integration
- Incident creation
- Clean Architecture
- SOLID principles
- Dependency Injection
- Async backend architecture
- PostgreSQL persistence

### Version 2 — Authentication & Enterprise Identity

Version 2 builds on the Version 1 foundation with:

- User registration and authentication
- JWT-based access control
- Secure password hashing
- Email verification
- Resend email integration
- ServiceNow `sys_user` verification
- Automatic enterprise approval
- Manual approval workflow
- ServiceNow user provisioning
- Webhook-based identity linking
- Protected incident creation
- Enterprise identity mapping
- Incident confirmation emails

### Version 3 — AI Copilot

The next stage extends the existing AI foundation toward:

- AI Copilot
- Context-aware ServiceNow assistance
- Knowledge Base integration
- Retrieval-Augmented Generation (RAG)
- Agentic AI workflows
- Human-in-the-loop automation
- Multi-agent orchestration

### Technology Stack

**FastAPI · Python · PostgreSQL · SQLAlchemy · Alembic · ServiceNow ·
Google Gemini · Ollama · JWT · Resend**

### Current Release

**Platform Version:** v0.2.0

**Platform Milestone:** Version 2

**API Version:** v1

**Base Path:** `/api/v1`

Use the endpoint groups below to explore the available APIs.
""",
        version=settings.application.version,
        contact={
            "name": "Ansh Taank",
            "email": "anshtaank24@gmail.com",
            "url": "https://github.com/ANSH-TAANK",
        },
        license_info={
            "name": "MIT License",
            "identifier": "MIT",
        },
        lifespan=lifespan,
    )

    # --------------------------------------------------------
    # Exception Handlers
    # --------------------------------------------------------

    register_exception_handlers(app)

    # --------------------------------------------------------
    # API Routes
    # --------------------------------------------------------

    app.include_router(api_router)

    # --------------------------------------------------------
    # Root Endpoint
    # --------------------------------------------------------

    @app.get(
        "/",
        include_in_schema=False,
    )
    def root() -> RedirectResponse:
        """
        Redirect users to Swagger UI.
        """

        return RedirectResponse(
            url="/docs",
            status_code=307,
        )

    # --------------------------------------------------------
    # Health Endpoint
    # --------------------------------------------------------

    @app.get(
        "/health",
        tags=["Health"],
        summary="Application Health Check",
    )
    def health() -> dict:
        """
        Verify that the application is running.
        """

        return {
            "status": "healthy",
            "application": settings.application.name,
            "version": settings.application.version,
        }

    logger.info("FastAPI application created.")

    return app


# ============================================================
# Application Instance
# ============================================================

app = create_app()
