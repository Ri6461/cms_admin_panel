"""Add parent_id column to roles table

Revision ID: 337836b539f8
Revises: 88273ae79005
Create Date: 2024-12-24 14:58:30.455122+05:45

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '337836b539f8'
down_revision: Union[str, None] = '88273ae79005'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add the parent_id column to the roles table
    op.add_column('roles', sa.Column('parent_id', sa.Integer(), sa.ForeignKey('roles.id'), nullable=True))


def downgrade() -> None:
    # Remove the parent_id column from the roles table
    op.drop_column('roles', 'parent_id')