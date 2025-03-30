from typing import Optional

from aiogram import Bot
from aiogram_i18n import I18nContext
from aiogram.types import (
    CallbackQuery, Chat, 
    User, Message
)

from bot.keyboards import ModerationCallback
from bot.database import get_locale
from .moderate_restricts import (
    unban_with_message, 
    unmute_with_message
)


async def handle_unmute_for_callback(
    bot: Bot, 
    i18n: I18nContext,
    callback: ModerationCallback,
    callback_query: CallbackQuery
) -> Optional[Message]:
    if not isinstance(callback_query.message, Message):
        return

    await callback_query.message.delete()

    user_id: int = callback.user_id
    admin_user: User = callback_query.from_user
    admin_full_name: str = admin_user.full_name
    chat: Chat = callback_query.message.chat
    locale: str = await get_locale(chat_id=chat.id)
    user_info = await bot.get_chat_member(
        chat_id=chat.id, 
        user_id=user_id
    )

    user: User = user_info.user

    await unmute_with_message(
        bot=bot,
        i18n=i18n,
        chat_id=chat.id,
        user_id=user.id,
        message_text=(
            i18n.get(
                "unmute-user",
                locale,
                user_id=user.id,
                admin_id=admin_user.id,
                user_full_name=user.full_name,
                admin_full_name=admin_full_name
            )
        )
    )


async def handle_unban_for_callback(
    bot: Bot,
    i18n: I18nContext,
    callback: ModerationCallback,
    callback_query: CallbackQuery
) -> Optional[Message]:
    if not isinstance(callback_query.message, Message):
        return

    await callback_query.message.delete()

    user_id: int = callback.user_id
    admin_user: User = callback_query.from_user
    admin_full_name: str = admin_user.full_name
    chat: Chat = callback_query.message.chat
    locale: str = await get_locale(chat_id=chat.id)
    user_info = await bot.get_chat_member(
        chat_id=chat.id, 
        user_id=user_id
    )

    user: User = user_info.user

    await unban_with_message(
        bot=bot,
        i18n=i18n,
        chat_id=chat.id,
        user_id=user.id,
        message_text=(
            i18n.get(
                "unban-user",
                locale,
                user_id=user.id,
                admin_id=admin_user.id,
                user_full_name=user.full_name,
                admin_full_name=admin_full_name
            )
        )
    )