"""Add permissions column to roles table

Revision ID: 88273ae79005
Revises: 7b3d12e9d2a0
Create Date: 2024-12-24 14:51:47.265713+05:45

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '88273ae79005'
down_revision: Union[str, None] = '7b3d12e9d2a0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add the permissions column to the roles table
    op.add_column('roles', sa.Column('permissions', sa.JSON(), nullable=True))


def downgrade() -> None:
    # Remove the permissions column from the roles table
    op.drop_column('roles', 'permissions')