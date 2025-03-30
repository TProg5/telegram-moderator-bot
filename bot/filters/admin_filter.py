from aiogram import Bot
from aiogram_i18n import I18nContext
from aiogram.types import ChatMember, Message
from functools import wraps

from bot.database import get_locale
from bot.utils import reply_message_and_delete


def is_admin(handler):
    @wraps(handler)
    async def wrapper(
        message: Message,
        # i18n: I18nContext, 
        *args, 
        **kwargs
    ):

        if not message.bot:
            return

        chat_id: int = message.chat.id
        user_id: int = message.from_user.id
        bot: Bot = message.bot
        # locale: str = await get_locale(chat_id=chat_id)
        member: ChatMember = await bot.get_chat_member(
            chat_id=chat_id, 
            user_id=user_id
        )

        # text: str = await i18n.get(
        #     "not-admin", 
        #     locale
        # )

        text = "You are not a administrator"

        if member.status in ["creator", "administrator"]:
            return await handler(message, *args, **kwargs)
        
        await reply_message_and_delete(
            chat_id=chat_id,
            bot=bot, 
            text=text,
            delay=10,
            message=message,
        )

    return wrapper