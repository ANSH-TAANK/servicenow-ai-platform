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
        summary="Enterprise AI-powered ServiceNow Incident Management Platform.",
        description="""
## Overview

An enterprise-grade platform that automates ServiceNow incident creation
using Large Language Models (LLMs). The platform is designed for
reliability, extensibility, maintainability, and production deployment.

---

## Core Capabilities

### 🤖 AI-Powered Incident Processing

Natural language understanding to extract structured incident information
from unstructured user requests, reducing manual effort and accelerating
incident resolution.

### 🎯 Intelligent Classification

Automatic prediction of:

- Category
- Subcategory
- Assignment Group
- Impact
- Urgency

using AI models combined with business rules.

### 🔄 Multi-Provider AI Support

Pluggable AI provider architecture supporting:

- Google Gemini
- Ollama
- Rule Engine (Automatic Fallback)

allowing organizations to select providers based on performance,
privacy, compliance, or infrastructure requirements.

### 🔌 ServiceNow REST API Integration

Direct integration with ServiceNow REST APIs for:

- Incident creation
- Incident updates
- Status synchronization
- Enterprise workflow automation.

---

## AI Failover Strategy

Gemini
↓

Ollama
↓

Rule Engine

If one provider becomes unavailable, the platform automatically switches
to the next provider without interrupting the incident creation workflow.

---

## Architecture

Built using modern software engineering practices including:

- Clean Architecture
- SOLID Principles
- Domain-Driven Design (DDD)
- Dependency Injection
- Strategy Pattern
- Provider Pattern
- Structured Exception Handling
- Request Validation
- Strongly Typed Data Models

The platform is organized into independent layers to maximize
testability, maintainability, and scalability.

---

## Future Roadmap

- LangGraph Agentic AI
- Retrieval-Augmented Generation (RAG)
- Human-in-the-loop Validation
- Knowledge Base Integration
- Multi-Agent Collaboration
- Authentication & Role-Based Access Control (RBAC)
- Kubernetes Deployment
- Distributed Tracing
- Metrics & Observability
- AI Analytics Dashboard

---

Built using Clean Architecture, SOLID Principles, and enterprise software
engineering best practices.
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
