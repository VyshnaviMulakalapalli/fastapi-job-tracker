"""Add email verification fields to User model

Revision ID: df225f59fde0
Revises: e1795eaf5d57
Create Date: 2025-03-03 18:16:37.974945

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'df225f59fde0'
down_revision: Union[str, None] = 'e1795eaf5d57'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add new columns instead of dropping the table
    op.add_column('users', sa.Column('is_verified', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('users', sa.Column('verification_token', sa.String(), nullable=True))

def downgrade():
    # Remove the columns if rolling back
    op.drop_column('users', 'verification_token')
    op.drop_column('users', 'is_verified')