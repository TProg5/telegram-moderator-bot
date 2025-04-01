from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware, Bot
from aiogram.types import (
    CallbackQuery, Chat, 
    Message, TelegramObject,
    InaccessibleMessage,
    ChatMemberAdministrator,
    ChatMemberOwner
)

from bot.utils import reply_message_and_delete


class CallbackAdminCheckerMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot):
        super().__init__()
        self.bot = bot

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, CallbackQuery):
            if event.message is None:
                await event.answer(
                    "The message related to this action is not available.",
                    show_alert=True,
                )
                return

            user_id: int = event.from_user.id
            chat: Chat = event.message.chat
            member = await self.bot.get_chat_member(
                chat_id=chat.id, 
                user_id=user_id
            )

            if not isinstance(member, (ChatMemberAdministrator, ChatMemberOwner)):
                await event.answer("Admins Only", show_alert=True)
                return
            
        return await handler(event, data)
    

class CallbackAdminCheckerMiddlewareV2:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        print("[DEBUG] ActionMiddleware triggered with data:", event.data)

        if isinstance(event, CallbackQuery):
            if event.message is None:
                await event.answer(
                    "The message related to this action is not available.",
                    show_alert=True,
                )
                return

            user_id: int = event.from_user.id
            chat_id: int = event.message.chat.id

            member = await self.bot.get_chat_member(chat_id=chat_id, user_id=user_id)

            if member.status not in ("administrator", "creator"):
                await event.answer("⛔ Admins Only", show_alert=True)
                return

        return await handler(event, data)
    

class AdminCheckerMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot):
        super().__init__()
        self.bot = bot

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, Message):
            if event.from_user is not None:
                user_id: int = event.from_user.id
                chat: Chat = event.chat
                member = await self.bot.get_chat_member(
                    chat_id=chat.id, 
                    user_id=user_id
                )
        
                if not isinstance(member, (ChatMemberAdministrator, ChatMemberOwner)):
                    await reply_message_and_delete(
                        bot=self.bot,
                        chat_id=chat.id,
                        text="You do not have sufficient rights to perform this function."
                    )

                return await handler(event, data)

        return await handler(event, data)