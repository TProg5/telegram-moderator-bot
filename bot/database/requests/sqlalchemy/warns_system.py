from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import update, Result, and_

from bot.database.models import Warns
from bot.database.engine import async_session


async def add_and_get_warns(
    user_id: int,
    chat_id: int
) -> int:
    async with async_session() as session:
        async with session.begin():
            result: Result = await session.execute(
                insert(Warns)
                .values(
                    user_id=user_id, 
                    chat_id=chat_id
                )
                .on_conflict_do_update(
                    where=Warns.warns < 3,
                    set_={"warns": Warns.warns + 1},
                    index_elements=[
                        "user_id", 
                        "chat_id"
                    ],
                )
                .returning(Warns.warns)
            )

            warns_count: int = result.scalar()
            if warns_count is None:
                return 1

            return warns_count
        

async def delete_warns(
    user_id: int,
    chat_id: int,
    warn: int = 1
) -> None:
    async with async_session() as session:
        async with session.begin():
            await session.execute(
                update(Warns)
                .values(warns=Warns.warns - warn)
                .where(
                    and_(
                        Warns.user_id == user_id,
                        Warns.chat_id == chat_id,
                        Warns.warns > 0
                    )
                )
            )


async def add_user(
        user_id: int,
        chat_id: int
    ) -> None:

    async with async_session() as session:
        async with session.begin():
            await session.execute(
                insert(Warns)
                .values(
                    user_id=user_id, 
                    chat_id=chat_id
                ).on_conflict_do_nothing(
                    index_elements=[
                        'user_id',
                        'chat_id'
                    ]
                )
            )
 