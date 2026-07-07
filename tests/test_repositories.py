"""
Repository Integration Tests

Purpose:
- Verify repository CRUD operations.
- Test integration with PostgreSQL.
- Validate repository behavior.
"""

import pytest

from app.infrastructure.database.models.user import User
from app.infrastructure.database.repositories.user import UserRepository

# ============================================================
# User Repository Tests
# ============================================================


class TestUserRepository:
    """
    Integration tests for UserRepository.
    """

    # ============================================================
    # Helper Methods
    # ============================================================

    def _create_user(
        self,
        suffix: str = "1",
    ) -> User:
        """
        Create a User entity with unique test data.

        Args:
            suffix:
                Unique suffix used to generate
                distinct usernames and emails.

        Returns:
            User entity.
        """

        return User(
            username=f"user_{suffix}",
            full_name=f"Test User {suffix}",
            email=f"user_{suffix}@example.com",
            is_servicenow_user=False,
        )

    # ============================================================
    # Create User
    # ============================================================

    @pytest.mark.asyncio
    async def test_create_user(
        self,
        db,
    ) -> None:
        """
        Verify that a user can be persisted successfully.
        """

        repository = UserRepository(db)

        # ---------------- Arrange ----------------

        user = self._create_user("create")

        created_user = await repository.create(user)

        await db.commit()

        # ---------------- Assert ----------------

        assert created_user.id is not None
        assert created_user.username == user.username
        assert created_user.full_name == user.full_name
        assert created_user.email == user.email
        assert created_user.is_servicenow_user is False

    # ============================================================
    # Get By ID
    # ============================================================

    @pytest.mark.asyncio
    async def test_get_by_id(
        self,
        db,
    ) -> None:
        """
        Verify that a user can be retrieved by ID.
        """

        repository = UserRepository(db)

        # ---------------- Arrange ----------------

        user = self._create_user("get_by_id")

        created = await repository.create(user)

        await db.commit()

        # ---------------- Act ----------------

        found = await repository.get_by_id(created.id)

        # ---------------- Assert ----------------

        assert found is not None
        assert found.id == created.id
        assert found.username == created.username

    # ============================================================
    # Get By Email
    # ============================================================

    @pytest.mark.asyncio
    async def test_get_by_email(
        self,
        db,
    ) -> None:
        """
        Verify that a user can be retrieved by email.
        """

        repository = UserRepository(db)

        # ---------------- Arrange ----------------

        user = self._create_user("email")

        await repository.create(user)

        await db.commit()

        # ---------------- Act ----------------

        found = await repository.get_by_email(user.email)

        # ---------------- Assert ----------------

        assert found is not None
        assert found.email == user.email

    # ============================================================
    # Get By Username
    # ============================================================

    @pytest.mark.asyncio
    async def test_get_by_username(
        self,
        db,
    ) -> None:
        """
        Verify that a user can be retrieved by username.
        """

        repository = UserRepository(db)

        # ---------------- Arrange ----------------

        user = self._create_user("username")

        await repository.create(user)

        await db.commit()

        # ---------------- Act ----------------

        found = await repository.get_by_username(user.username)

        # ---------------- Assert ----------------

        assert found is not None
        assert found.username == user.username

    # ============================================================
    # Get By ServiceNow sys_id
    # ============================================================

    @pytest.mark.asyncio
    async def test_get_by_servicenow_sys_id(
        self,
        db,
    ) -> None:
        """
        Verify that a user can be retrieved by ServiceNow sys_id.
        """

        repository = UserRepository(db)

        # ---------------- Arrange ----------------

        user = self._create_user("servicenow")
        user.servicenow_sys_id = "SYS123456789"

        await repository.create(user)

        await db.commit()

        # ---------------- Act ----------------

        found = await repository.get_by_servicenow_sys_id(
            "SYS123456789",
        )

        # ---------------- Assert ----------------

        assert found is not None
        assert found.servicenow_sys_id == "SYS123456789"

    # ============================================================
    # Get All
    # ============================================================

    @pytest.mark.asyncio
    async def test_get_all(
        self,
        db,
    ) -> None:
        """
        Verify that users can be retrieved using get_all().
        """

        repository = UserRepository(db)

        # ---------------- Arrange ----------------

        await repository.create(self._create_user("all1"))
        await repository.create(self._create_user("all2"))

        await db.commit()

        # ---------------- Act ----------------

        users = await repository.get_all()

        # ---------------- Assert ----------------

        assert len(users) >= 2

    # ============================================================
    # Exists
    # ============================================================

    @pytest.mark.asyncio
    async def test_exists(
        self,
        db,
    ) -> None:
        """
        Verify that exists() correctly detects matching users.
        """

        repository = UserRepository(db)

        # ---------------- Arrange ----------------

        user = self._create_user("exists")

        await repository.create(user)

        await db.commit()

        # ---------------- Act ----------------

        result = await repository.exists(
            User.email == user.email,
        )

        # ---------------- Assert ----------------

        assert result is True

    # ============================================================
    # Count
    # ============================================================

    @pytest.mark.asyncio
    async def test_count(
        self,
        db,
    ) -> None:
        """
        Verify that count() returns the number of users.
        """

        repository = UserRepository(db)

        # ---------------- Arrange ----------------

        initial_count = await repository.count()

        await repository.create(self._create_user("count"))

        await db.commit()

        # ---------------- Act ----------------

        new_count = await repository.count()

        # ---------------- Assert ----------------

        assert new_count == initial_count + 1

    # ============================================================
    # Update
    # ============================================================

    @pytest.mark.asyncio
    async def test_update(
        self,
        db,
    ) -> None:
        """
        Verify that user updates are persisted.
        """

        repository = UserRepository(db)

        # ---------------- Arrange ----------------

        user = self._create_user("update")

        created = await repository.create(user)

        await db.commit()

        # ---------------- Act ----------------

        created.full_name = "Updated Name"

        updated = await repository.update(created)

        await db.commit()

        # ---------------- Assert ----------------

        assert updated.full_name == "Updated Name"

    # ============================================================
    # Hard Delete
    # ============================================================

    @pytest.mark.asyncio
    async def test_hard_delete(
        self,
        db,
    ) -> None:
        """
        Verify that a user can be permanently deleted.
        """

        repository = UserRepository(db)

        # ---------------- Arrange ----------------

        user = self._create_user("delete")

        created = await repository.create(user)

        await db.commit()

        # ---------------- Act ----------------

        await repository.hard_delete(created)

        await db.commit()

        deleted = await repository.get_by_id(created.id)

        # ---------------- Assert ----------------

        assert deleted is None
