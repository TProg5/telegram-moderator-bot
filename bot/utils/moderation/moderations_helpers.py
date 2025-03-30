import asyncio
from datetime import datetime
from typing import Optional, List 

from aiogram import Bot
from aiogram_i18n import I18nContext
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import ChatPermissions, Message

from bot.database import get_locale
from ..helpers import (
    send_unrestriction_message,
    reply_message_and_delete
)


async def unban_with_message(
    bot: Bot,
    i18n: I18nContext, 
    chat_id: int, 
    user_id: int,
    message_text: str,
    message: Optional[Message] = None
) -> Message:
    try:
        await bot.unban_chat_member(
            chat_id=chat_id, 
            user_id=user_id
        )

    except TelegramBadRequest:
        await reply_message_and_delete(
            bot=bot,
            chat_id=chat_id,
            message=message,
            text=i18n.get(
                "error-unban",
                await get_locale(
                    chat_id=chat_id
                )
            )
        )

    await reply_message_and_delete(
        bot=bot,
        chat_id=chat_id,
        text=message_text,
        message=message
    )


async def unmute_with_message(
    bot: Bot,
    i18n: I18nContext, 
    chat_id: int, 
    user_id: int,
    message_text: str,
    message: Optional[Message] = None
) -> Message:
    try:
        await bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            permissions=ChatPermissions(can_send_messages=True)
        )

    except TelegramBadRequest:
        await reply_message_and_delete(
            bot=bot,
            chat_id=chat_id,
            message=message,
            text=i18n.get(
                "error-unmute",
                await get_locale(
                    chat_id=chat_id
                )
            )
        )

    await reply_message_and_delete(
        bot=bot,
        chat_id=chat_id,
        text=message_text,
        message=message
    )


async def ban_with_message(
    bot: Bot,
    i18n: I18nContext, 
    chat_id: int, 
    user_id: int,
    message_text: str,
    buttons_text: Optional[List[str]] = None,
    callback_data: Optional[List[str]] = None,
    buttons_level: Optional[int] = None,
    until_date: Optional[datetime] = None,
    message: Optional[Message] = None
) -> Message:
    try:
        await bot.ban_chat_member(
            chat_id=chat_id, 
            user_id=user_id, 
            until_date=until_date
        )

    except TelegramBadRequest:
        await reply_message_and_delete(
            bot=bot,
            chat_id=chat_id,
            message=message,
            text=i18n.get(
                "error-ban",
                await get_locale(
                    chat_id=chat_id
                )
            )
        )

    asyncio.create_task(
        send_unrestriction_message(
            bot=bot, 
            chat_id=chat_id,
            i18n=i18n,
            user_id=user_id, 
            end_time=until_date
        )
    )

    await reply_message_and_delete(
        bot=bot,
        chat_id=chat_id,
        text=message_text,
        buttons_text=buttons_text,
        callback_data=callback_data,
        buttons_level=buttons_level,
        message=message
    )


async def mute_with_message(
    bot: Bot,
    i18n: Optional[I18nContext], 
    chat_id: int,
    user_id: int,  
    message_text: str,
    buttons_text: Optional[List[str]] = None,
    callback_data: Optional[List[str]] = None,
    buttons_level: Optional[int] = None,
    until_date: Optional[datetime] = None,
    message: Optional[Message] = None
) -> Message:
    try:
        await bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            permissions=ChatPermissions(can_send_messages=False),
            until_date=until_date,
        )

    except TelegramBadRequest:
        if not i18n:
            return await reply_message_and_delete(
                bot=bot,
                chat_id=chat_id,
                text="Mute error",
            )

        await reply_message_and_delete(
            bot=bot,
            chat_id=chat_id,
            message=message,
            text=i18n.get(
                "error-mute",
                await get_locale(
                    chat_id=chat_id
                )
            )
        )

    asyncio.create_task(
        send_unrestriction_message(
            bot=bot, 
            i18n=i18n,
            chat_id=chat_id, 
            user_id=user_id, 
            end_time=until_date
        )
    )

    await reply_message_and_delete(
        bot=bot,
        chat_id=chat_id,
        text=message_text,
        buttons_text=buttons_text,
        callback_data=callback_data,
        buttons_level=buttons_level,
        message=message
    )