from typing import Optional
import re

from aiogram import Bot, Router, F
from aiogram.filters import Command, CommandObject
from aiogram_i18n import I18nContext
from aiogram.types import (
    Message, CallbackQuery, 
    InaccessibleMessage,
    Chat
)

from bot.database import get_locale, add_chat_info
from bot.keyboards import ModerationCallback, LanguageCallback
from bot.utils import (
    handler_to_ban, handler_to_mute, 
    handler_to_unban, handler_to_unmute,
    handle_unban_for_callback,
    handle_unmute_for_callback,
    reply_message_and_delete
)

admin_command = Router()


@admin_command.message(Command("mute"))
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
        i18n=i18n,
        message=message,
        command=command
    )


@admin_command.message(Command("ban"))
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
async def unmute_callback(
    callback_query: CallbackQuery,
    callback_data: ModerationCallback,
    i18n: I18nContext
) -> None:
    bot: Optional[Bot] = callback_query.bot
    if not bot:
        return None
    
    await handle_unmute_for_callback(
        bot=bot,
        i18n=i18n,
        callback=callback_data,
        callback_query=callback_query
    )


@admin_command.callback_query(ModerationCallback.filter(F.action == "unban"))
async def unban_callback(
    callback_query: CallbackQuery,
    callback_data: ModerationCallback,
    i18n: I18nContext
) -> None:
    bot: Optional[Bot] = callback_query.bot
    if not bot:
        return None

    await handle_unban_for_callback(
        bot=bot,
        i18n=i18n,
        callback=callback_data,
        callback_query=callback_query
    )


@admin_command.message(Command('set_language'))
async def set_language(
    message: Message,
    i18n: I18nContext
) -> Optional[Message]:
    bot: Optional[Bot] = message.bot
    if not bot:
        return None
    
    await reply_message_and_delete(
        bot=bot,
        chat_id=message.chat.id,
        buttons_level=3,
        buttons_text=[
            "🇬🇧Englisg",
            "🇷🇺Russian"
        ],
        callback_data=[
            LanguageCallback(language="en").pack(),
            LanguageCallback(language="ru").pack()
        ],
        text=i18n.get(
            "set-language",
            await get_locale(
                chat_id=message.chat.id
            )
        )
    )


@admin_command.callback_query(LanguageCallback.filter())
async def set_language_callback(
    callback_query: CallbackQuery,
    callback_data: LanguageCallback,
    i18n: I18nContext
) -> Optional[Message]:
    if isinstance(callback_query.message, InaccessibleMessage) or not callback_query.message:
        return None
    
    if not callback_query.bot:
        return None
    
    await callback_query.message.delete()
    
    bot: Bot = callback_query.bot
    message: Message = callback_query.message

    await add_chat_info(
        chat_id=message.chat.id,
        locale=callback_data.language
    )

    await reply_message_and_delete(
        bot=bot,
        chat_id=message.chat.id,
        text=i18n.get(
            "success-language",
            locale=await get_locale(
                chat_id=message.chat.id
            )
        )
    )


@admin_command.message(Command("set_rules"))
async def help_handler(
    message: Message, 
    command: CommandObject,
    i18n: I18nContext
) -> None:
    message_id: Optional[str] = command.args
    chat: Chat = message.chat
    bot: Optional[Bot] = message.bot
    locale: str = await get_locale(
        chat_id=chat.id
    )

    if not bot:
        print("LOG:NOT A BOT")
        return None


    if not message.reply_to_message:
        await reply_message_and_delete(
            bot=bot,
            chat_id=message.chat.id,
            message=message,
            text=i18n.get(
                "error-reply-rule",
                await get_locale(
                    chat_id=message.chat.id
                )
            )
        )

    
    # if not message_id or not re.fullmatch(r"\d+", message_id):
    #     await reply_message_and_delete(
    #         bot=bot,
    #         chat_id=chat.id,
    #         text=i18n.get(
    #             "error-rule",
    #             locale=locale
    #         )
    #     )
    #     return
    

    # message_id_int: int = int(message_id)
    message_reply_id: int = message.reply_to_message.from_user.id

    await add_chat_info(
        chat_id=chat.id, 
        message_id=message_reply_id # message_id_int
    )

    await reply_message_and_delete(
        bot=bot,
        chat_id=chat.id,
        text=i18n.get(
            "success-rule",
            locale=locale
        ),
        message=message
    )