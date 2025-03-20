import logging

from typing import (
    Any, Callable, 
    Dict, Awaitable,
)


from aiogram import BaseMiddleware, Bot
from aiogram.types import (
    TelegramObject, ChatMemberUpdated, 
    User, Update
)
from aiogram.types import Message

from bot.database.requests.users_requests import add_user


class WelcomeMiddleware(BaseMiddleware):
    def __init__(self, bot):
        BaseMiddleware.__init__(self)
        self.bot = bot

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        
        try:
            if hasattr(event, 'chat_member') and isinstance(event.chat_member, ChatMemberUpdated):
                member: ChatMemberUpdated = event.chat_member
                user: User = member.new_chat_member.user
                user_id: int = member.from_user.id

                if member.new_chat_member.status == "member" and member.old_chat_member.status == "member":
                    chat_id = member.chat.id

                    await self.bot.send_message(
                        chat_id=chat_id,
                        text=f"👋 <b>Welcome, {user.full_name}!</b>",
                        parse_mode="HTML"
                    )

                    await add_user(user_id)
            else:
                logging.warning(f"Unexpected event type: {event}")

        except Exception as e:
            logging.error(f"Error in WelcomeMiddleware: {e}")

        return await handler(event, data)