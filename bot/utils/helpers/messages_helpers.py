import asyncio
from typing import Optional
from datetime import datetime
from contextlib import suppress

from aiogram import Bot
from aiogram.filters.callback_data import CallbackData
from aiogram.exceptions import TelegramBadRequest
from aiogram_i18n import I18nContext
from aiogram.types import (
    ChatMemberMember, 
    Message, ChatMember
)

from bot.keyboards import moderation_keyboard


async def auto_delete(
    message: Message, 
    delay: float = 30.0
) -> None: 
    with suppress(TelegramBadRequest, AttributeError): 
        await asyncio.sleep(delay) 
        await message.delete() 


async def reply_message_and_delete( 
    chat_id: int,
    bot: Bot,
    text: str, 
    delay: float = 30.0,
    message: Optional[Message] = None,
    button_text: Optional[str] = None,
    action: Optional[str] = None,
    user_id: Optional[int] = None
) -> Message:
    
    reply_message: Message = await bot.send_message(
        text=text,
        chat_id=chat_id,
        reply_markup=await moderation_keyboard(
            text=button_text,
            action=action,
            user_id=user_id
        )
    ) 

    await auto_delete(
        message=reply_message, 
        delay=delay
    ) 

    if message: 
        await auto_delete(
            message=message, 
            delay=delay
        )

    return reply_message


async def send_unrestriction_message(
    bot: Bot,
    i18n: I18nContext,
    chat_id: int,
    user_id: int, 
    new_datetime: Optional[datetime]
) -> None:
    if not new_datetime:
        return

    wait_time: float = (new_datetime - datetime.now()).total_seconds()
    chat_member: ChatMember = await bot.get_chat_member(
        chat_id=chat_id, 
        user_id=user_id
    )

    if wait_time <= 0:
        await reply_message_and_delete(
            bot=bot,
            chat_id=chat_id,
            text=i18n.get(
                "error-time"
            )
        )

    await asyncio.sleep(wait_time)

    if isinstance(chat_member, ChatMemberMember):
        await reply_message_and_delete(
            bot=bot,
            chat_id=chat_id,
            text=(
                i18n.get(
                    "unmute-user",
                    user_id=user_id,
                    user_full_name=chat_member.user.full_name
                )
            )
        )