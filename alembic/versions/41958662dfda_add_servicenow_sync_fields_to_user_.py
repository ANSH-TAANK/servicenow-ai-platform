"""add servicenow sync fields to user approvals

Revision ID: 41958662dfda
Revises: 5f383273eaee
Create Date: 2026-07-28 22:43:14.351254

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "41958662dfda"
down_revision: Union[str, Sequence[str], None] = "5f383273eaee"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # ============================================================
    # Add ServiceNow synchronization columns
    # ============================================================

    op.add_column(
        "user_approvals",
        sa.Column(
            "servicenow_sync_status",
            sa.Enum(
                "PENDING",
                "SYNCED",
                "FAILED",
                "RETRYING",
                name="servicenowsyncstatus",
                native_enum=False,
            ),
            nullable=False,
            server_default="PENDING",
        ),
    )

    op.add_column(
        "user_approvals",
        sa.Column(
            "servicenow_sys_id",
            sa.String(length=32),
            nullable=True,
        ),
    )

    op.add_column(
        "user_approvals",
        sa.Column(
            "servicenow_number",
            sa.String(length=50),
            nullable=True,
        ),
    )

    op.add_column(
        "user_approvals",
        sa.Column(
            "servicenow_sync_error",
            sa.String(length=1000),
            nullable=True,
        ),
    )

    op.add_column(
        "user_approvals",
        sa.Column(
            "retry_count",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )

    # ============================================================
    # Indexes & Constraints
    # ============================================================

    op.create_index(
        op.f("ix_user_approvals_servicenow_sync_status"),
        "user_approvals",
        ["servicenow_sync_status"],
        unique=False,
    )

    op.create_unique_constraint(
        "uq_user_approvals_servicenow_sys_id",
        "user_approvals",
        ["servicenow_sys_id"],
    )

    # ============================================================
    # Remove temporary defaults
    # ============================================================

    op.alter_column(
        "user_approvals",
        "servicenow_sync_status",
        server_default=None,
    )

    op.alter_column(
        "user_approvals",
        "retry_count",
        server_default=None,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint(
        "uq_user_approvals_servicenow_sys_id",
        "user_approvals",
        type_="unique",
    )

    op.drop_index(
        op.f("ix_user_approvals_servicenow_sync_status"),
        table_name="user_approvals",
    )

    op.drop_column(
        "user_approvals",
        "retry_count",
    )

    op.drop_column(
        "user_approvals",
        "servicenow_sync_error",
    )

    op.drop_column(
        "user_approvals",
        "servicenow_number",
    )

    op.drop_column(
        "user_approvals",
        "servicenow_sys_id",
    )

    op.drop_column(
        "user_approvals",
        "servicenow_sync_status",
    )
