from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    BigInteger, Integer,
    PrimaryKeyConstraint,
    UniqueConstraint,
    String
)

from bot.database.engine import Base


class ChatManager(Base):
    __tablename__ = 'chats_manager'
    __table_args__ = {
        PrimaryKeyConstraint(
            "id",
            name='primary_id_const'
        ),
        UniqueConstraint(
            'chat_id', 
            name='unique_chat_const'
        )
    }

    id: Mapped[int] = mapped_column(Integer)
    chat_id: Mapped[int] = mapped_column(BigInteger)
    message_id: Mapped[int] = mapped_column(BigInteger, nullable=True, default=None),
    locale: Mapped[str] = mapped_column(String(10), default="en")