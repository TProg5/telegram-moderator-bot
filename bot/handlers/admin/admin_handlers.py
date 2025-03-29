from typing import Optional

from aiogram import Bot, Router, F
from aiogram.filters import Command, CommandObject
from aiogram_i18n import I18nContext
from aiogram.types import Message, CallbackQuery

from bot.keyboards import ModerationCallback
from bot.filters.admin_filter import is_admin
from bot.database import get_locale
from bot.utils import (
    handler_to_ban, handler_to_mute, 
    handler_to_unban, handler_to_unmute,
    handle_unban_for_callback,
    handle_unmute_for_callback,
    reply_message_and_delete
)


admin_command = Router()


@admin_command.message(Command("mute"))
@is_admin
async def mute_user(
    message: Message, 
    command: CommandObject,
    i18n: I18nContext
) -> Optional[Message]:
    bot: Optional[Bot] = message.bot
    if not bot:
        return None

    if not message.reply_to_message:
        await reply_message_and_delete(
            bot=bot,
            chat_id=message.chat.id,
            message=message,
            text=i18n.get(
                "error-reply",
                await get_locale(
                    chat_id=message.chat.id
                )
            )
        )

    await handler_to_mute(
        bot=bot, 
        message=message,
        i18n=i18n,
        command=command
    )


@admin_command.message(Command("ban"))
@is_admin
async def ban_user(
    message: Message, 
    command: CommandObject,
    i18n: I18nContext
) -> Optional[Message]:
    bot: Optional[Bot] = message.bot
    if not bot:
        return None

    if not message.reply_to_message:
        await reply_message_and_delete(
            bot=bot,
            chat_id=message.chat.id,
            message=message,
            text=i18n.get(
                "error-reply",
                await get_locale(
                    chat_id=message.chat.id
                )
            )
        )

    await handler_to_ban(
        bot=bot, 
        message=message,
        i18n=i18n,
        command=command
    )


@admin_command.message(Command("unmute"))
@is_admin
async def unmute_user(
    message: Message,
    i18n: I18nContext
) -> Optional[Message]:
    bot: Optional[Bot] = message.bot
    if not bot:
        return None

    if not message.reply_to_message:
        await reply_message_and_delete(
            bot=bot,
            chat_id=message.chat.id,
            message=message,
            text=i18n.get(
                "error-reply",
                await get_locale(
                    chat_id=message.chat.id
                )
            )
        )

    await handler_to_unmute(
        bot=bot, 
        message=message,
        i18n=i18n
    )


@admin_command.message(Command("unban"))
@is_admin
async def unban_user(
    message: Message,
    i18n: I18nContext
) -> Optional[Message]:
    bot: Optional[Bot] = message.bot
    if not bot:
        return None

    if not message.reply_to_message:
        await reply_message_and_delete(
            bot=bot,
            chat_id=message.chat.id,
            message=message,
            text=i18n.get(
                "error-reply",
                await get_locale(
                    chat_id=message.chat.id
                )
            )
        )

    await handler_to_unban(
        bot=bot, 
        message=message,
        i18n=i18n
    )


@admin_command.callback_query(ModerationCallback.filter(F.action == "unmute"))
@is_admin
async def unmute_callback(
    callback_query: CallbackQuery,
    callback_data: ModerationCallback,
    i18n: I18nContext
) -> None:
    pass



@admin_command.callback_query(ModerationCallback.filter(F.action == "unban"))
@is_admin
async def unban_callback(
    callback_query: CallbackQuery,
    callback_data: ModerationCallback,
    i18n: I18nContext
) -> None:
    pass