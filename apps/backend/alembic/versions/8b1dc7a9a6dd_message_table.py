"""message table

Revision ID: 8b1dc7a9a6dd
Revises: ab5bb0976c66
Create Date: 2026-11-27 15:51:04.505584

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8b1dc7a9a6dd'
down_revision: Union[str, Sequence[str], None] = 'ab5bb0976c66'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "message",
        sa.Column("message_id", sa.Integer(), primary_key=True),
        sa.Column("service_id", sa.Integer(), sa.ForeignKey("ongoing_service.service_id"), nullable=False),
        sa.Column("sender_id", sa.UUID(), sa.ForeignKey("users.user_id"), nullable=False),
        sa.Column("message", sa.String(length=1000), nullable=False),
        sa.Column("delivered_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("read_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_message_service_id", "message", ["service_id"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("message")
