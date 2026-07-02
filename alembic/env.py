from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

# Import all ORM models so they are registered with Base.metadata
import app.infrastructure.database.models  # noqa: F401
from alembic import context
from app.core.config import settings
from app.infrastructure.database.base import Base

# ============================================================
# Alembic Configuration
# ============================================================

config = context.config

# Use the application's database configuration
config.set_main_option(
    "sqlalchemy.url",
    settings.database.url,
)

# ============================================================
# Logging
# ============================================================

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ============================================================
# SQLAlchemy Metadata
# ============================================================

target_metadata = Base.metadata


# ============================================================
# Offline Migrations
# ============================================================


def run_migrations_offline() -> None:
    """
    Run migrations in offline mode.
    """

    context.configure(
        url=settings.database.url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# ============================================================
# Online Migrations
# ============================================================


def run_migrations_online() -> None:
    """
    Run migrations in online mode.
    """

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# ============================================================
# Entry Point
# ============================================================

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
