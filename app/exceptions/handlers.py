"""
Global Exception Handlers

Purpose:
- Register all application exception handlers.
- Convert application exceptions into consistent HTTP responses.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions.base import BaseApplicationException

# ============================================================
# Register Exception Handlers
# ============================================================


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register all global exception handlers.
    """

    @app.exception_handler(BaseApplicationException)
    async def handle_application_exception(
        request: Request,
        exc: BaseApplicationException,
    ) -> JSONResponse:
        """
        Handle all custom application exceptions.
        """

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": exc.error_code,
                    "message": exc.message,
                },
            },
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_exception(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        """
        Handle unexpected exceptions.
        """

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected error occurred.",
                },
            },
        )
