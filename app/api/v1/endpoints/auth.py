"""
Authentication API Endpoints

Purpose:
- Expose REST endpoints for platform authentication.
- Handle user registration and login.
- Provide JWT authentication endpoints.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, Form, status

from app.api.dependencies.auth import get_auth_service, get_current_user_id
from app.application.auth.requests import (
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
)
from app.application.auth.responses import LoginResponse, UserResponse
from app.application.auth.service import AuthenticationService
from app.core.logging import get_logger

logger = get_logger(__name__)

# ============================================================
# Router
# ============================================================

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

# ============================================================
# Register
# ============================================================


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register User",
    description="Create a new platform user.",
)
async def register(
    request: RegisterRequest,
    service: AuthenticationService = Depends(
        get_auth_service,
    ),
) -> UserResponse:
    """
    Register a new platform user.
    """

    logger.info("Received user registration request.")

    response = await service.register(
        request,
    )

    logger.info(
        "User '%s' registered successfully.",
        response.username,
    )

    return response


# ============================================================
# Login
# ============================================================


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Login",
    description="Authenticate a platform user.",
)
async def login(
    request: LoginRequest,
    service: AuthenticationService = Depends(
        get_auth_service,
    ),
) -> LoginResponse:
    """
    Authenticate a platform user.
    """

    logger.info("Received login request.")

    response = await service.login(
        request,
    )

    logger.info("User logged in successfully.")

    return response


# ============================================================
# OAuth2 Token
# ============================================================


@router.post(
    "/token",
    response_model=LoginResponse,
    summary="OAuth2 Access Token",
    description="OAuth2-compatible login endpoint for Swagger UI.",
)
async def oauth2_token(
    username: str = Form(...),
    password: str = Form(...),
    service: AuthenticationService = Depends(
        get_auth_service,
    ),
) -> LoginResponse:
    """
    OAuth2 password flow endpoint.

    Swagger UI submits form data using the OAuth2 password
    specification. Internally we reuse the existing
    authentication service.
    """

    logger.info(
        "Received OAuth2 token request.",
    )

    response = await service.login(
        LoginRequest(
            email=username,
            password=password,
        ),
    )

    logger.info(
        "OAuth2 authentication successful.",
    )

    return response


# ============================================================
# Refresh Token
# ============================================================


@router.post(
    "/refresh",
    response_model=LoginResponse,
    summary="Refresh Access Token",
    description="Generate a new access token using a refresh token.",
)
async def refresh(
    request: RefreshTokenRequest,
    service: AuthenticationService = Depends(
        get_auth_service,
    ),
) -> LoginResponse:
    """
    Refresh authentication tokens.
    """

    logger.info("Received token refresh request.")

    response = await service.refresh(
        request,
    )

    logger.info("Authentication tokens refreshed.")

    return response


# ============================================================
# Current User
# ============================================================


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Current User",
    description="Retrieve the currently authenticated user.",
)
async def get_current_user(
    current_user_id: UUID = Depends(get_current_user_id),
    service: AuthenticationService = Depends(
        get_auth_service,
    ),
) -> UserResponse:
    """
    Retrieve the currently authenticated user.
    """

    logger.info(
        "Current user information requested.",
    )

    response = await service.get_current_user(
        current_user_id,
    )

    return response
