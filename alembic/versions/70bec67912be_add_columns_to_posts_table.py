"""add columns to posts table

Revision ID: 70bec67912be
Revises: 6477a1f209b5
Create Date: 2023-08-15 14:42:40.295425

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '70bec67912be'
down_revision: Union[str, None] = '6477a1f209b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
