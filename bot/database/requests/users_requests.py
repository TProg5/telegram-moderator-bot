import asyncio

from typing import Any

from bot.database.__all_models import Users
from bot.database.base_model import async_session

from sqlalchemy.dialects.postgresql import insert

from sqlalchemy import Insert, Select, Update, Delete


async def add_user(tg_id: int) -> None:
    async with async_session() as session:
        async with session.begin():
            await session.execute(
                insert(Users)
                .values(id_telegram=tg_id)
                .on_conflict_do_nothing(
                    index_elements = [
                        "id_telegram"
                    ]
                )
            )


