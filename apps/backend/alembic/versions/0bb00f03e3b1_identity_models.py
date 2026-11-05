"""identity models

Revision ID: 0bb00f03e3b1
Revises: 0c1b89fe3ff2
Create Date: 2026-09-24 14:40:04.592075

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "0bb00f03e3b1"
down_revision: Union[str, Sequence[str], None] = "0c1b89fe3ff2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "association",
        sa.Column("asso_id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=15), nullable=False),
        sa.PrimaryKeyConstraint("asso_id"),
    )

    op.create_table(
        "permission",
        sa.Column("asso_id", sa.String(length=36), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["asso_id"],
            ["association.asso_id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint(
            "asso_id",
            "user_id",
        ),
    )
    op.create_table(
        "picture",
        sa.Column("picture_id", sa.Integer(), nullable=False, autoincrement=True),
        sa.Column("asso_id", sa.String(length=36), nullable=False),
        sa.Column("path", sa.String(length=500), nullable=False),
        sa.ForeignKeyConstraint(
            ["asso_id"],
            ["association.asso_id"],
        ),
        sa.PrimaryKeyConstraint("picture_id"),
    )
    op.create_table(
        "list_service",
        sa.Column("list_service_id", sa.Integer(), nullable=False, autoincrement=True),
        sa.Column("asso_id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("approximative_cost", sa.Integer(), nullable=False),
        sa.Column("approximative_time", sa.String(length=50), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=False),
        sa.Column("path", sa.String(length=512), nullable=False),
        sa.ForeignKeyConstraint(
            ["asso_id"],
            ["association.asso_id"],
        ),
        sa.PrimaryKeyConstraint("list_service_id"),
    )
    op.create_table(
        "ongoing_service",
        sa.Column("service_id", sa.Integer(), nullable=False, autoincrement=True),
        sa.Column("asso_id", sa.String(length=36), nullable=False),
        sa.Column("client_id", sa.Integer(), nullable=False),
        sa.Column("type_service_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("end_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(length=25), nullable=False),
        sa.Column("context", sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(
            ["asso_id"],
            ["association.asso_id"],
        ),
        sa.ForeignKeyConstraint(
            ["client_id"],
            ["users.id"],
        ),
        sa.ForeignKeyConstraint(
            ["type_service_id"],
            ["list_service.list_service_id"],
        ),
        sa.PrimaryKeyConstraint("service_id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("permission")
    op.drop_table("ongoing_service")
    op.drop_table("picture")
    op.drop_table("list_service")
    op.add_column(
        "users", sa.Column("disabled_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column(
        "users",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.add_column(
        "users",
        sa.Column(
            "is_admin", sa.Boolean(), server_default=sa.text("false"), nullable=False
        ),
    )
    op.alter_column("users", "last_name", type_=sa.String())
    op.alter_column("users", "first_name", type_=sa.String())
    op.alter_column("users", "email", type_=sa.String())
