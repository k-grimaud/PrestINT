"""service_template

Revision ID: 18d771b4722f
Revises: 8b1dc7a9a6dd
Create Date: 2026-11-27 19:03:04.229004

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


# revision identifiers, used by Alembic.
revision: str = '18d771b4722f'
down_revision: Union[str, Sequence[str], None] = '8b1dc7a9a6dd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("list_service", sa.Column("template", JSONB(), server_default="[]", nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("list_service", "template")
