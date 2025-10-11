"""add user table

Revision ID: 6a5f624680c2
Revises: ba074046d08a
Create Date: 2025-10-11 15:35:37.631906

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6a5f624680c2'
down_revision: Union[str, Sequence[str], None] = 'ba074046d08a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users', 
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True), 
                    sa.Column('email', sa.String(), nullable=False, unique=True), 
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), 
                            nullable=False,server_default=sa.text('now()'))
                            
                    )
    

    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
