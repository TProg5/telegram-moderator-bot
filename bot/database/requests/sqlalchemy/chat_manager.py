from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import Result, select

from bot.database.models import ChatManager
from bot.database.engine import async_session


async def add_chat_info(
    chat_id: int,
    locale: str = "en",
    message_id: int = None
) -> None:
    async with async_session() as session:
        async with session.begin():
            if message_id:
                await session.execute(
                    insert(ChatManager)
                    .values(
                        chat_id=chat_id,
                        message_id=message_id
                    )
                    .on_conflict_do_update(
                        set_={"message_id": message_id},
                        index_elements=["chat_id"]
                    )
                )

            if locale:
                await session.execute(
                    insert(ChatManager)
                    .values(
                        chat_id=chat_id,
                        locale=locale
                    )
                    .on_conflict_do_update(
                        set_={"locale": locale},
                        index_elements=["chat_id"]
                    )
                )

    
async def get_message_id(chat_id: int) -> int:
    async with async_session() as session:
        async with session.begin():
            result: Result = await session.execute(
                select(ChatManager.message_id)
                .where(ChatManager.chat_id == chat_id)
            )

            message_id: int = result.scalar()
            return message_id


async def get_locale(chat_id: int) -> str:
    async with async_session() as session:
        async with session.begin():
            result: Result = await session.execute(
                select(ChatManager.locale)
                .where(ChatManager.chat_id == chat_id)
            )

            locale: int = result.scalar()
            return locale