"""identity models

Revision ID: 0bb00f03e3b1
Revises: 0c1b89fe3ff2
Create Date: 2026-09-24 14:40:04.592075

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '0bb00f03e3b1'
down_revision: Union[str, Sequence[str], None] = '0c1b89fe3ff2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # renamed, not dropped: the FKs from sessions/audit_events follow the rename
    op.alter_column('users', 'id', new_column_name='user_id')
    op.alter_column('users', 'email', type_=sa.String(length=255))
    op.alter_column('users', 'first_name', type_=sa.String(length=50))
    op.alter_column('users', 'last_name', type_=sa.String(length=50))
    op.drop_column('users', 'is_admin')
    op.drop_column('users', 'created_at')
    op.drop_column('users', 'disabled_at')
    op.create_table('list_service',
    sa.Column('list_service_id', sa.UUID(), nullable=False),
    sa.Column('asso_id', sa.UUID(), nullable=False),
    sa.Column('path', sa.String(length=500), nullable=False),
    sa.PrimaryKeyConstraint('list_service_id')
    )
    op.create_table('picture',
    sa.Column('picture_id', sa.UUID(), nullable=False),
    sa.Column('asso_id', sa.UUID(), nullable=False),
    sa.Column('path', sa.String(length=500), nullable=False),
    sa.PrimaryKeyConstraint('picture_id')
    )
    op.create_table('ongoing_service',
    sa.Column('service_id', sa.UUID(), nullable=False),
    sa.Column('asso_id', sa.UUID(), nullable=False),
    sa.Column('client_id', sa.UUID(), nullable=False),
    sa.Column('presta_id', sa.UUID(), nullable=False),
    sa.Column('type_presta_id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('end_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('status', sa.String(length=25), nullable=False),
    sa.Column('context', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['client_id'], ['users.user_id'], ),
    sa.ForeignKeyConstraint(['presta_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('service_id')
    )
    op.create_table('permission',
    sa.Column('asso_id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('permission', sa.String(length=30), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('asso_id', 'user_id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('permission')
    op.drop_table('ongoing_service')
    op.drop_table('picture')
    op.drop_table('list_service')
    op.add_column('users', sa.Column('disabled_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('users', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False))
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), server_default=sa.text('false'), nullable=False))
    op.alter_column('users', 'last_name', type_=sa.String())
    op.alter_column('users', 'first_name', type_=sa.String())
    op.alter_column('users', 'email', type_=sa.String())
    op.alter_column('users', 'user_id', new_column_name='id')
