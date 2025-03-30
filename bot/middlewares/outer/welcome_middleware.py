import logging
from typing import (
    Any, Callable, 
    Dict, Awaitable,
)

from aiogram_i18n import I18nContext
from aiogram import BaseMiddleware, Bot
from aiogram.types import (
    TelegramObject, ChatMemberUpdated, 
    User, Update
)


class WelcomeMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot):
        
        self.bot: Bot = bot

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any], 
        
    ) -> Any:

        try:
            if isinstance(event, ChatMemberUpdated):
                member: ChatMemberUpdated = event
                new_member = member.new_chat_member
                old_member = member.old_chat_member
                
                user: User = new_member.user

                if new_member.status == "member" or old_member.status == "left":
                    chat_id = member.chat.id

                    await self.bot.send_message(
                        chat_id=chat_id,
                        text=f"👋 <b>Welcome</b>, <a href='tg://user?id={user.id}'><b>{user.full_name}</b></a>",
                        parse_mode="HTML"
                    )
                    
            else:
                logging.warning(f"Unexpected event type: {event}")

        except Exception as e:
            logging.error(f"Error in WelcomeMiddleware: {e}")

        return await handler(event, data)