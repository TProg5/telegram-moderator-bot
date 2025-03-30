"""huynya_ebanaya2

Revision ID: ab73fe3df959
Revises: af43a9393eac
Create Date: 2025-03-29 20:06:30.558273

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ab73fe3df959'
down_revision: Union[str, None] = 'af43a9393eac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'warns_system',
        sa.Column('id', sa.Integer()),
        sa.Column('user_id', sa.BigInteger()),
        sa.Column('chat_id', sa.BigInteger()),
        sa.Column('warns', sa.Integer(), default=1),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint(
            'user_id', 
            'chat_id', 
            name='unique_chat_user_const'
        ),
    )


def downgrade() -> None:
    op.drop_table('warns_system')