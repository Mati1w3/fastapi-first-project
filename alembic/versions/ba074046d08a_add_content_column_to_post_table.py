"""add content column to post table

Revision ID: ba074046d08a
Revises: 5cec75555fb3
Create Date: 2025-10-11 15:30:48.565785

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ba074046d08a'
down_revision: Union[str, Sequence[str], None] = '5cec75555fb3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
