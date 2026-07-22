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

from datetime import UTC, datetime, timedelta
from uuid import UUID

from pwdlib.exceptions import UnknownHashError
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.approval.exceptions import UserApprovalPendingError
from app.application.approval.service import ApprovalService
from app.application.auth.exceptions import (
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    UserInactiveError,
    UsernameAlreadyExistsError,
    UserNotFoundError,
    UserNotVerifiedError,
    VerificationAlreadyCompletedError,
    VerificationCodeExpiredError,
    VerificationCodeInvalidError,
    VerificationCodeNotFoundError,
)
from app.application.auth.requests import (
    ForgotPasswordRequest,
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
    ResendVerificationRequest,
    ResetPasswordRequest,
    UpdateUsernameRequest,
    VerifyEmailRequest,
    VerifyResetOTPRequest,
)
from app.application.auth.responses import (
    LoginResponse,
    MessageResponse,
    UsernameAvailabilityResponse,
    UserResponse,
)
from app.application.auth.username_suggestions import UsernameSuggestionGenerator
from app.application.auth.validators import (
    normalize_email,
    normalize_username,
    validate_password,
    validate_username,
)
from app.core.constants import BEARER_TOKEN_TYPE, VERIFICATION_CODE_EXPIRATION_MINUTES
from app.core.logging import get_logger
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    generate_verification_code,
    hash_password,
    hash_verification_code,
    verify_password,
    verify_verification_code,
)
from app.domain.verification.enums import VerificationPurpose, VerificationStatus
from app.infrastructure.database.models.user import User
from app.infrastructure.database.models.verification_code import VerificationCode
from app.infrastructure.database.repositories.user import UserRepository
from app.infrastructure.database.repositories.verification_code_repository import (
    VerificationCodeRepository,
)

logger = get_logger(__name__)

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
        self._users = UserRepository(
            db,
        )
        self._verification_codes = VerificationCodeRepository(
            db,
        )
        self._username_generator = UsernameSuggestionGenerator()

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
            username=username,
            full_name=request.full_name,
            email=email,
            password_hash=hash_password(
                request.password,
            ),
        )

        user = await self._users.create(
            user,
        )

        verification_code = generate_verification_code()

        logger.info(
            "Email verification code for %s: %s",
            user.email,
            verification_code,
        )

        verification = VerificationCode(
            user_id=user.id,
            purpose=VerificationPurpose.EMAIL_VERIFICATION,
            status=VerificationStatus.PENDING,
            code_hash=hash_verification_code(
                verification_code,
            ),
            expires_at=self._calculate_verification_expiration(),
        )

        await self._verification_codes.create(
            verification,
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
        Authenticate a platform user using
        an email address or username.
        """

        try:
            user = await self._get_user_by_identifier(
                request.identifier,
            )

        except UserNotFoundError as exc:
            raise InvalidCredentialsError(
                "Invalid identifier or password.",
            ) from exc

        if not user.password_hash:
            raise InvalidCredentialsError(
                "Invalid identifier or password.",
            )

        try:
            password_valid = verify_password(
                request.password,
                user.password_hash,
            )

        except UnknownHashError as exc:
            raise InvalidCredentialsError(
                "Invalid identifier or password.",
            ) from exc

        if not user.is_verified:
            raise UserNotVerifiedError()

        approval_service = ApprovalService(
            self._db,
        )

        if not await approval_service.can_user_login(
            user.id,
        ):
            raise UserApprovalPendingError()

        if not password_valid:
            raise InvalidCredentialsError(
                "Invalid identifier or password.",
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

    async def update_username(
        self,
        user_id: UUID,
        request: UpdateUsernameRequest,
    ) -> UserResponse:
        """
        Update the authenticated user's username.
        """

        user = await self._get_user_by_id(
            user_id,
        )

        username = normalize_username(
            request.username,
        )

        validate_username(
            username,
        )

        if user.username == username:
            return UserResponse.model_validate(
                user,
            )

        if await self._username_exists(
            username,
        ):

            suggestions = await self._find_available_usernames(
                username,
            )

            raise UsernameAlreadyExistsError(
                suggestions=suggestions,
            )

        user.username = username

        await self._users.update(
            user,
        )

        await self._db.commit()

        return UserResponse.model_validate(
            user,
        )

    async def check_username_availability(
        self,
        username: str,
    ) -> UsernameAvailabilityResponse:
        """
        Check whether a username is available.

        If unavailable, return alternative
        username suggestions.
        """

        username = normalize_username(
            username,
        )

        validate_username(
            username,
        )

        if not await self._username_exists(
            username,
        ):
            return UsernameAvailabilityResponse(
                username=username,
                available=True,
                suggestions=[],
            )

        suggestions = await self._find_available_usernames(
            username,
        )

        return UsernameAvailabilityResponse(
            username=username,
            available=False,
            suggestions=suggestions,
        )

    async def _username_exists(
        self,
        username: str,
    ) -> bool:
        """
        Determine whether a username
        already exists.
        """

        user = await self._users.get_by_username(
            username,
        )

        return user is not None

    async def _find_available_usernames(
        self,
        username: str,
        *,
        limit: int = 3,
    ) -> list[str]:
        """
        Find available username suggestions.

        Args:
            username:
                Requested username.

            limit:
                Maximum number of suggestions.

        Returns:
            Available username suggestions.
        """

        available: list[str] = []

        generator_limit = max(
            limit * 5,
            20,
        )

        candidates = self._username_generator.generate(
            username,
            limit=generator_limit,
        )

        for candidate in candidates:

            if await self._username_exists(
                candidate,
            ):
                continue

            available.append(
                candidate,
            )

            if (
                len(
                    available,
                )
                >= limit
            ):
                break

        return available

    async def verify_email(
        self,
        request: VerifyEmailRequest,
    ) -> MessageResponse:

        user = await self._get_user_by_identifier(
            request.email,
        )

        verification = await self._get_latest_verification_code(
            user,
            VerificationPurpose.EMAIL_VERIFICATION,
        )
        self._ensure_verification_not_completed(
            verification,
        )

        self._ensure_verification_not_expired(
            verification,
        )
        if not verify_verification_code(
            request.verification_code,
            verification.code_hash,
        ):
            raise VerificationCodeInvalidError()

        await self._mark_email_verified(
            user,
            verification,
        )

        approval_service = ApprovalService(
            self._db,
        )

        await approval_service.create_initial_approval(
            user.id,
        )

        await self._db.commit()

        return MessageResponse(
            message="Email verified successfully.",
        )

    # ============================================================
    # Private Methods
    # ============================================================

    def _calculate_verification_expiration(
        self,
    ) -> datetime:
        """
        Calculate when a verification code expires.
        """

        return datetime.now(UTC) + timedelta(
            minutes=VERIFICATION_CODE_EXPIRATION_MINUTES,
        )

    async def _get_latest_verification_code(
        self,
        user: User,
        purpose: VerificationPurpose,
    ) -> VerificationCode:
        """
        Retrieve the latest verification code for a user.
        """

        verification = await self._verification_codes.get_latest_by_user_and_purpose(
            user_id=user.id,
            purpose=purpose,
        )

        if verification is None:
            raise VerificationCodeNotFoundError()

        return verification

    def _ensure_verification_not_completed(
        self,
        verification: VerificationCode,
    ) -> None:
        """
        Ensure the verification code has not already been used.
        """

        if verification.status == VerificationStatus.VERIFIED:
            raise VerificationAlreadyCompletedError()

    def _ensure_verification_not_expired(
        self,
        verification: VerificationCode,
    ) -> None:
        """
        Ensure the verification code has not expired.
        """

        if verification.expires_at < datetime.now(
            UTC,
        ):
            raise VerificationCodeExpiredError()

    async def _mark_email_verified(
        self,
        user: User,
        verification: VerificationCode,
    ) -> None:
        """
        Mark a user's email as verified.
        """

        user.is_verified = True

        verification.status = VerificationStatus.VERIFIED

        verification.verified_at = datetime.now(
            UTC,
        )

        await self._users.update(
            user,
        )

        await self._verification_codes.update(
            verification,
        )

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
            raise EmailAlreadyExistsError()

        if await self._username_exists(
            username,
        ):

            suggestions = await self._find_available_usernames(
                username,
            )

            raise UsernameAlreadyExistsError(
                suggestions=suggestions,
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

        self._ensure_user_is_active(
            user,
        )

        return user

    async def _get_user_by_identifier(
        self,
        identifier: str,
    ) -> User:
        """
        Retrieve a user using an email address
        or username.
        """

        if "@" in identifier:
            email = normalize_email(
                identifier,
            )

            user = await self._users.get_by_email(
                email,
            )

        else:
            username = normalize_username(
                identifier,
            )

            user = await self._users.get_by_username(
                username,
            )

        if user is None:
            raise UserNotFoundError(
                "User does not exist.",
            )

        self._ensure_user_is_active(
            user,
        )

        return user

    def _ensure_user_is_active(
        self,
        user: User,
    ) -> None:
        """
        Ensure the user account is active.
        """

        if not user.is_active:
            raise UserInactiveError(
                "User account is inactive.",
            )

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
