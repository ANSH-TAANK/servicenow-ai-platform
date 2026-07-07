"""
Authentication Service

Purpose:
- Handle authentication business logic.
- Coordinate validation, repositories, and security.
- Authenticate platform users.

This module DOES NOT:
- Define API routes.
- Access HTTP requests directly.
- Call ServiceNow APIs.
"""

from datetime import UTC, datetime
from uuid import UUID

from pwdlib.exceptions import UnknownHashError
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.auth.exceptions import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
    UserInactiveError,
    UserNotFoundError,
)
from app.application.auth.requests import (
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
)
from app.application.auth.responses import LoginResponse, UserResponse
from app.application.auth.validators import (
    normalize_email,
    normalize_username,
    validate_password,
    validate_username,
)
from app.core.constants import BEARER_TOKEN_TYPE
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    hash_password,
    verify_password,
)
from app.infrastructure.database.models.user import User
from app.infrastructure.database.repositories.user import UserRepository

# ============================================================
# Authentication Service
# ============================================================


class AuthenticationService:
    """
    Handles authentication business logic.
    """

    # ============================================================
    # Constructor
    # ============================================================

    def __init__(
        self,
        db: AsyncSession,
    ) -> None:
        """
        Initialize the authentication service.
        """

        self._db = db
        self._users = UserRepository(db)

    # ============================================================
    # Public Methods
    # ============================================================

    async def register(
        self,
        request: RegisterRequest,
    ) -> UserResponse:
        """
        Register a new platform user.
        """

        email = normalize_email(
            request.email,
        )

        username = normalize_username(
            request.username,
        )

        validate_username(
            username,
        )

        validate_password(
            request.password,
        )

        await self._ensure_user_does_not_exist(
            email=email,
            username=username,
        )

        user = User(
            username=request.username,
            full_name=request.full_name,
            email=email,
            password_hash=hash_password(
                request.password,
            ),
        )

        user = await self._users.create(
            user,
        )

        await self._db.commit()

        return UserResponse.model_validate(
            user,
        )

    async def login(
        self,
        request: LoginRequest,
    ) -> LoginResponse:
        """
        Authenticate a platform user.
        """

        email = normalize_email(
            request.email,
        )

        try:
            user = await self._get_user_by_email(
                email,
            )

        except UserNotFoundError as exc:
            raise InvalidCredentialsError(
                "Invalid email or password.",
            ) from exc

        if not user.password_hash:
            raise InvalidCredentialsError(
                "Invalid email or password.",
            )

        try:
            password_valid = verify_password(
                request.password,
                user.password_hash,
            )

        except UnknownHashError as exc:
            raise InvalidCredentialsError(
                "Invalid email or password.",
            ) from exc

        if not password_valid:
            raise InvalidCredentialsError(
                "Invalid email or password.",
            )

        user.last_login_at = datetime.now(
            UTC,
        )

        await self._users.update(
            user,
        )

        await self._db.commit()

        return self._generate_tokens(
            user,
        )

    async def refresh(
        self,
        request: RefreshTokenRequest,
    ) -> LoginResponse:
        """
        Refresh JWT tokens.
        """

        payload = decode_refresh_token(
            request.refresh_token,
        )

        try:
            user = await self._get_user_by_id(
                UUID(payload["sub"]),
            )

        except UserNotFoundError as exc:
            raise InvalidCredentialsError(
                "Invalid refresh token.",
            ) from exc

        return self._generate_tokens(
            user,
        )

    async def _get_user_by_id(
        self,
        user_id: UUID,
    ) -> User:
        """
        Retrieve a user by ID or raise an exception.
        """

        user = await self._users.get_by_id(
            user_id,
        )

        if user is None:
            raise UserNotFoundError(
                "User does not exist.",
            )

        if not user.is_active:
            raise UserInactiveError(
                "User account is inactive.",
            )

        return user

    async def get_current_user(
        self,
        user_id: UUID,
    ) -> UserResponse:
        """
        Retrieve the currently authenticated user.
        """

        user = await self._get_user_by_id(
            user_id,
        )

        return UserResponse.model_validate(
            user,
        )

    # ============================================================
    # Private Methods
    # ============================================================

    async def _ensure_user_does_not_exist(
        self,
        email: str,
        username: str,
    ) -> None:
        """
        Ensure a user with the given email or username
        does not already exist.
        """

        existing_user = await self._users.get_by_email(
            email,
        )

        if existing_user is not None:
            raise UserAlreadyExistsError(
                "A user with this email already exists.",
            )

        existing_user = await self._users.get_by_username(
            username,
        )

        if existing_user is not None:
            raise UserAlreadyExistsError(
                "A user with this username already exists.",
            )

    async def _get_user_by_email(
        self,
        email: str,
    ) -> User:
        """
        Retrieve a user or raise an exception.
        """

        user = await self._users.get_by_email(
            email,
        )

        if user is None:
            raise UserNotFoundError(
                "User does not exist.",
            )

        if not user.is_active:
            raise UserInactiveError(
                "User account is inactive.",
            )

        return user

    def _generate_tokens(
        self,
        user: User,
    ) -> LoginResponse:
        """
        Generate authentication tokens.
        """

        access_token = create_access_token(
            subject=str(user.id),
        )

        refresh_token = create_refresh_token(
            subject=str(user.id),
        )

        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type=BEARER_TOKEN_TYPE,
        )
