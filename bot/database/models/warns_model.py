from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    BigInteger, Integer,
    PrimaryKeyConstraint,
    UniqueConstraint
)

from bot.database.engine import Base


class Warns(Base):
    __tablename__ = 'warns_system'
    __table_args__ = (
        PrimaryKeyConstraint(
            "id",
            name='primary_id_const'
        ),
        UniqueConstraint(
            'chat_id', 
            'user_id', 
            name='unique_chat_user_const'
        )
    )

    id: Mapped[int] = mapped_column(Integer)
    warns: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    chat_id: Mapped[int] = mapped_column(BigInteger)
    user_id: Mapped[int] =  mapped_column(BigInteger)