from typing import Optional

from aiogram import Bot
from aiogram.types import ChatMember, Message
from functools import wraps

from bot.utils.helpers.messages_helpers import reply_message_and_delete

def is_admin(handler):
    @wraps(handler)
    async def wrapper(message: Message, *args, **kwargs):

        chat_id: int = message.chat.id
        user_id: int = message.from_user.id

        bot: Bot = message.bot
        
        text: str = "You are not a group administrator"

        member: ChatMember = await message.bot.get_chat_member(
            chat_id=chat_id, 
            user_id=user_id
        )

        if member.status in ["creator", "administrator"]:
            return await handler(message, *args, **kwargs)
        
        await reply_message_and_delete(
            chat_id=chat_id,
            bot=bot, 
            text=text,
            delay=10,
            message=message,
            user_id=user_id
        )

    return wrapper