"""permission column

Revision ID: ab5bb0976c66
Revises: 98bb5c373a7a
Create Date: 2026-11-27 13:47:06.111626

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ab5bb0976c66'
down_revision: Union[str, Sequence[str], None] = '98bb5c373a7a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("permission", sa.Column("permission", sa.String(length=15), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("permission", "permission")
