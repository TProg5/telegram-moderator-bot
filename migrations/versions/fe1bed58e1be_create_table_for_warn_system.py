"""Create table for warn system

Revision ID: fe1bed58e1be
Revises: 
Create Date: 2025-03-15 17:23:00.885282

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fe1bed58e1be'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'warns_system',
        sa.Column('id', sa.Integer()),
        sa.Column('user_id', sa.Integer()),
        sa.Column('chat_id', sa.Integer()),
        sa.Column('warns', sa.Integer(), default=0),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint(
            'user_id', 
            'chat_id', 
            name='unique_chat_user_const'
        ),
    )


def downgrade() -> None:
    op.drop_table('warns_system')