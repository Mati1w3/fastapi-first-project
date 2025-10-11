"""add last few columns to post table

Revision ID: 1d673efdc2da
Revises: 6dd1a41704f9
Create Date: 2025-10-11 15:49:30.989265

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1d673efdc2da'
down_revision: Union[str, Sequence[str], None] = '6dd1a41704f9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', 
                                     sa.Boolean(), 
                                     nullable=False, 
                                     server_default='TRUE'))
    
    op.add_column('posts', sa.Column('created_at', 
                                     sa.TIMESTAMP(timezone=True), 
                                     nullable=False, 
                                     server_default=sa.text('now()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
