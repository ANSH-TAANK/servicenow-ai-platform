"""
Global Exception Handlers

Purpose:
- Register all application exception handlers.
- Convert application exceptions into consistent HTTP responses.
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.core.constants import INTERNAL_SERVER_ERROR_CODE, INTERNAL_SERVER_ERROR_MESSAGE
from app.core.logging import get_logger
from app.exceptions.base import BaseApplicationException

logger = get_logger(__name__)

# ============================================================
# Register Exception Handlers
# ============================================================


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register all global exception handlers.
    """

    @app.exception_handler(BaseApplicationException)
    async def handle_application_exception(
        _request: Request,
        exc: BaseApplicationException,
    ) -> JSONResponse:
        """
        Handle all custom application exceptions.
        """

        content = {
            "success": False,
            "error": {
                "code": exc.error_code,
                "message": exc.message,
            },
        }

        if exc.details is not None:
            content.update(
                exc.details,
            )

        return JSONResponse(
            status_code=exc.status_code,
            content=content,
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_exception(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        """
        Handle unexpected exceptions.
        """

        logger.exception(
            "Unhandled exception while processing request %s %s.",
            request.method,
            request.url.path,
        )

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": {
                    "code": INTERNAL_SERVER_ERROR_CODE,
                    "message": INTERNAL_SERVER_ERROR_MESSAGE,
                },
            },
        )
