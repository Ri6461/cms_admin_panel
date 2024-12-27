"""Add role_id column to users table

Revision ID: 7b3d12e9d2a0
Revises: 
Create Date: 2024-12-19 14:35:04.370404+05:45

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '7b3d12e9d2a0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add the role_id column to the users table
    op.add_column('users', sa.Column('role_id', sa.Integer(), sa.ForeignKey('roles.id'), nullable=True))


def downgrade() -> None:
    # Remove the role_id column from the users table
    op.drop_column('users', 'role_id')