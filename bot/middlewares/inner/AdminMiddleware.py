from typing import Any, Awaitable, Callable, Dict

from aiogram_i18n import I18nContext
from aiogram import BaseMiddleware, Bot
from aiogram.types import CallbackQuery, Chat, Message, TelegramObject

from utils.spacy_functions.filter_messages import get_locale


class CallbackAdminCheckerMiddleware:
    def __init__(
            self, 
            bot: Bot,
            i18n: I18nContext
        ):

        self.bot = bot
        self.i18n = i18n

    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        
        print("[DEBUG] ActionMiddleware triggered with data:", event.data)

        if not isinstance(event, CallbackQuery) or event.message is None:
            return await handler(event, data)

        user_id: int = event.from_user.id
        chat_id: int = event.message.chat.id

        member = await self.bot.get_chat_member(
            chat_id=chat_id, user_id=user_id
            )

        text = self.i18n.get(
            "not-admin-callback",  # Важно! Данной локализации не существует, нужно добавить
            await get_locale(
                    chat_id=chat_id
                )
        )
        
        if member.status not in ("administrator", "creator"):
            await event.answer("Admins Only", show_alert=True)
            return

        return await handler(event, data)