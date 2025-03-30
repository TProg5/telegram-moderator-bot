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

from utils.spacy_functions.filter_messages import get_locale


class WelcomeMiddleware(BaseMiddleware):
    def __init__(
            self, 
            bot: Bot,
            i18n: I18nContext
        ):
        
        self.bot: Bot = bot
        self.i18n = i18n

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any], 
        
    ) -> Any:

        try:
            if isinstance(event.chat_member, ChatMemberUpdated):
                member: ChatMemberUpdated = event.chat_member
                user: User = member.new_chat_member.user
                user_id: int = member.from_user.id

                if member.new_chat_member.status == "member":
                    chat_id = member.chat.id

                    text=self.i18n.get(
                        "welcome-user", # Важно! Данной локализации не существует, нужно добавить
                        await get_locale(
                            chat_id=chat_id
                        )
                    )

                    await self.bot.send_message(
                        chat_id=chat_id,
                        text=f"👋 <b>Welcome, {user.full_name}!</b>",
                        parse_mode="HTML"
                    )
                    
                    
            else:
                logging.warning(f"Unexpected event type: {event}")

        except Exception as e:
            logging.error(f"Error in WelcomeMiddleware: {e}")

        return await handler(event, data)