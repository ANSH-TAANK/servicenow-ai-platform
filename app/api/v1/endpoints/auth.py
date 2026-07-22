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
    UpdateUsernameRequest,
    VerifyEmailRequest,  # NEW
)
from app.application.auth.responses import (
    LoginResponse,
    MessageResponse,  # NEW
    UsernameAvailabilityResponse,
    UserResponse,
)
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


@router.post(
    "/verify-email",
    response_model=MessageResponse,
    summary="Verify Email",
    description="Verify a user's email address using the verification code.",
)
async def verify_email(
    request: VerifyEmailRequest,
    service: AuthenticationService = Depends(
        get_auth_service,
    ),
) -> MessageResponse:
    """
    Verify a user's email address.
    """

    logger.info(
        "Email verification requested for %s.",
        request.email,
    )

    response = await service.verify_email(
        request,
    )

    logger.info(
        "Email verified successfully for %s.",
        request.email,
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
            identifier=username,
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


# ============================================================
# Username Availability
# ============================================================


@router.get(
    "/username/availability",
    response_model=UsernameAvailabilityResponse,
    summary="Check Username Availability",
    description="Determine whether a username is available and return suggestions if it is already taken.",
)
async def check_username_availability(
    username: str,
    service: AuthenticationService = Depends(
        get_auth_service,
    ),
) -> UsernameAvailabilityResponse:
    """
    Check whether a username is available.
    """

    logger.info(
        "Checking username availability for '%s'.",
        username,
    )

    return await service.check_username_availability(
        username,
    )


# ============================================================
# Update Username
# ============================================================


@router.patch(
    "/username",
    response_model=UserResponse,
    summary="Update Username",
    description="Update the authenticated user's platform username.",
)
async def update_username(
    request: UpdateUsernameRequest,
    current_user_id: UUID = Depends(
        get_current_user_id,
    ),
    service: AuthenticationService = Depends(
        get_auth_service,
    ),
) -> UserResponse:
    """
    Update the authenticated user's username.
    """

    logger.info(
        "Username update requested by user %s.",
        current_user_id,
    )

    response = await service.update_username(
        user_id=current_user_id,
        request=request,
    )

    logger.info(
        "Username updated successfully for user %s.",
        current_user_id,
    )

    return response
