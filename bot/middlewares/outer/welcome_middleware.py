from typing import (
    Any, Callable, 
    Dict, Awaitable,
)

from aiogram import BaseMiddleware, Bot
from aiogram.types import (
    TelegramObject, ChatMemberUpdated, 
    User, Update, ChatMember
)

from bot.utils import reply_message_and_delete


class WelcomeMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any], 
    ) -> Any:
        if isinstance(event, ChatMemberUpdated):
            new_member: ChatMember = event.new_chat_member
            old_member: ChatMember = event.old_chat_member
            user: User = new_member.user

            if new_member.status == "member" or old_member.status == "left":
                chat_id: int = event.chat.id

                await reply_message_and_delete(
                    chat_id=chat_id,
                    text=f"👋<b>Welcome <a href='tg://user?id={user.id}'>{user.full_name}</a></b>",
                )

            return await handler(event, data)
        return await handler(event, data)