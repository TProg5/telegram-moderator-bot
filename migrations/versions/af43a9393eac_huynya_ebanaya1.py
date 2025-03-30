"""huynya_ebanaya1

Revision ID: af43a9393eac
Revises: 
Create Date: 2025-03-29 20:06:22.409889

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'af43a9393eac'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "chats_manager",
        sa.Column("id", sa.Integer),
        sa.Column("chat_id", sa.BigInteger),
        sa.Column("rules_id", sa.BigInteger, default=None, nullable=True),
        sa.Column("locale", sa.String(10), default="en"),
        sa.PrimaryKeyConstraint(
            "id",
            name="primary_id_const"
        ),
        sa.UniqueConstraint(
            "chat_id", 
            name="unique_chat_const"
        )
    )


def downgrade() -> None:
    op.drop_table("chats_manager")