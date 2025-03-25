import asyncio
from datetime import datetime
from typing import Optional

from aiogram import Bot
from aiogram_i18n import I18nContext
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import ChatPermissions, Message

from bot.database import get_locale
from bot.utils.helpers import (
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
    button_text: Optional[str] = None,
    action: Optional[str] = None,
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
            user_id=user_id, 
            new_datetime=until_date
        )
    )

    await reply_message_and_delete(
        bot=bot,
        chat_id=chat_id,
        text=message_text,
        action=action,
        user_id=user_id,
        button_text=button_text,
        message=message
    )


async def mute_with_message(
    bot: Bot,
    i18n: I18nContext, 
    chat_id: int,
    user_id: int,  
    message_text: str,
    button_text: Optional[str] = None,
    action: Optional[str] = None,
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
            chat_id=chat_id, 
            user_id=user_id, 
            new_datetime=until_date
        )
    )

    await reply_message_and_delete(
        bot=bot,
        chat_id=chat_id,
        text=message_text,
        user_id=user_id,
        action=action,
        button_text=button_text,
        message=message
    )