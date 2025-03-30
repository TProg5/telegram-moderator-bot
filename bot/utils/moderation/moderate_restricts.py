import re
from datetime import datetime, timedelta
from typing import (
    Tuple, Union, 
    Optional
)

from aiogram import Bot
from aiogram.filters import CommandObject
from aiogram.types import Message, User
from aiogram_i18n import I18nContext

from ..helpers import reply_message_and_delete
from bot.keyboards import ModerationCallback
from bot.database import get_locale
from .moderations_helpers import (
    unmute_with_message,
    unban_with_message,
    mute_with_message,
    ban_with_message
)


def parse_time_and_reason(
    args: str,
    i18n: I18nContext
) -> Union[Tuple[datetime, str, str], Tuple[None, None, None]]:
    if not args:
        return None, None, None
    
    match: Optional[re.Match] = re.match(r"(\d+\s*[mhdw])\s*(.*)", args.lower().strip())
    if not match:
        return None, None, None

    time_string: str = match.group(1).strip()
    reason: str = match.group(2).strip()

    match = re.match(r"(\d+)\s*([mhdw])", time_string)
    if not match:
        return None, None, None

    value, unit = int(match.group(1)), match.group(2)
    current_datetime = datetime.now()

    if unit == "m":
        time_delta: timedelta = timedelta(minutes=value)
        readable_time: str = f"{value} {i18n.get("minutes1") if value > 1 else i18n.get("minutes2")}"
    elif unit == "h":
        time_delta: timedelta = timedelta(hours=value)
        readable_time: str = f"{value} {i18n.get("hours1") if value > 1 else i18n.get("hours2")}"
    elif unit == "d":
        time_delta: timedelta = timedelta(days=value)
        readable_time: str = f"{value} {i18n.get("days1") if value > 1 else i18n.get("days2")}"
    elif unit == "w":
        time_delta: timedelta = timedelta(weeks=value)
        readable_time: str = f"{value} {i18n.get("weeks1") if value > 1 else i18n.get("weeks2")}"
    else:
        return None, None, None

    until_date: datetime = current_datetime + time_delta
    if not reason:
        reason = i18n.get("error-reason")
    return until_date, readable_time, reason


async def handler_to_mute(
    bot: Bot, 
    i18n: I18nContext,
    message: Message,
    command: CommandObject
) -> Message:
    if not message.reply_to_message.from_user:
        await reply_message_and_delete(
            bot=bot,
            message=message,
            chat_id=message.chat.id,
            text=i18n.get(
                "error-reply",
                await get_locale(
                    chat_id=message.chat.id
                )
            )
        )

    if not command.args:
        await reply_message_and_delete(
            bot=bot,
            message=message,
            chat_id=message.chat.id,
            text=i18n.get(
                "error-args",
                await get_locale(
                    chat_id=message.chat.id
                )
            )
        )

    reply_user: User = message.reply_to_message.from_user
    admin_user: User = message.from_user
    chat_id: int = message.chat.id
    user_id: int = reply_user.id
    user_full_name: str = reply_user.full_name
    admin_full_name: str = admin_user.full_name
    locale: str = await get_locale(chat_id=chat_id)
    until_date, readable_time, reason = parse_time_and_reason(
        args=command.args,
        i18n=i18n
    )

    if not until_date or not readable_time:
        await reply_message_and_delete(
            bot=bot,
            message=message,
            chat_id=chat_id,
            text=i18n.get(
                "error-args",
                locale
            )
        )

    await mute_with_message(
        bot=bot,
        chat_id=chat_id,
        i18n=i18n,
        user_id=user_id,
        until_date=until_date,
        callback_data=[
            ModerationCallback(
                action='unmute',
                user_id=user_id
            ).pack()
        ],
        buttons_text=[
            i18n.get(
                'unmute-button',
                locale
            )
        ],
        message_text=i18n.get(
            "mute-user",
            locale,
            user_id=user_id,
            user_full_name=user_full_name, 
            admin_full_name=admin_full_name,
            admin_id=admin_user.id,
            time=until_date, 
            readable_time=readable_time, 
            reason=reason
        )
    )


async def handler_to_ban(
    bot: Bot,
    i18n: I18nContext,
    message: Message,
    command: CommandObject
) -> Message:

    if not message.reply_to_message.from_user or not message.from_user:
        await reply_message_and_delete(
            bot=bot,
            message=message,
            chat_id=message.chat.id,
            text=i18n.get(
                "error-reply",
                await get_locale(
                    chat_id=message.chat.id
                )
            )
        )

    if not command.args:
        await reply_message_and_delete(
            bot=bot,
            message=message,
            chat_id=message.chat.id,
            text=i18n.get(
                "error-args",
                await get_locale(
                    chat_id=message.chat.id
                )
            )
        )

    reply_user: User = message.reply_to_message.from_user
    admin_user: User = message.from_user
    chat_id: int = message.chat.id
    user_id: int = reply_user.id
    user_full_name: str = reply_user.full_name
    admin_full_name: str = admin_user.full_name
    locale: str = await get_locale(chat_id=chat_id)
    until_date, readable_time, reason = parse_time_and_reason(
        args=command.args,
        i18n=i18n
    )

    if not until_date or not readable_time:
        await reply_message_and_delete(
            bot=bot,
            message=message,
            chat_id=chat_id,
            text=i18n.get(
                "error-args",
                locale
            )
        )

    await ban_with_message(
        bot=bot,
        chat_id=chat_id,
        i18n=i18n,
        user_id=user_id,
        until_date=until_date,
        callback_data=[
            ModerationCallback(
                action='unban',
                user_id=user_id
            ).pack()
        ],
        buttons_text=[
            i18n.get(
                'unban-button',
                locale
            )
        ],
        message_text=i18n.get(
            "ban-user",
            locale,
            user_id=user_id,
            user_full_name=user_full_name,
            admin_full_name=admin_full_name,
            admin_id=admin_user.id,
            time=until_date,
            readable_time=readable_time,
            reason=reason
        )
    )


async def handler_to_unmute(
    bot: Bot,
    i18n: I18nContext,
    message: Message
) -> Message:
    if not message.reply_to_message.from_user or not message.from_user:
        await reply_message_and_delete(
            bot=bot,
            message=message,
            chat_id=message.chat.id,
            text=i18n.get(
                "error-reply",
                await get_locale(
                    chat_id=message.chat.id
                )
            )
        )

    reply_user: User = message.reply_to_message.from_user
    admin_user: User = message.from_user
    chat_id: int = message.chat.id
    user_id: int = reply_user.id
    user_full_name: str = reply_user.full_name
    admin_full_name: str = admin_user.full_name
    locale: str = await get_locale(chat_id=chat_id)

    await unmute_with_message(
        bot=bot,
        chat_id=chat_id,
        user_id=user_id,
        i18n=i18n,
        message_text=i18n.get(
            "unmute-user",
            locale,
            user_id=user_id,
            user_full_name=user_full_name,
            admin_full_name=admin_full_name,
            admin_id=admin_user.id
        )
    )


async def handler_to_unban(
    bot: Bot, 
    i18n: I18nContext,
    message: Message
) -> Message:
    if not message.reply_to_message.from_user or not message.from_user:
        await reply_message_and_delete(
            bot=bot,
            message=message,
            chat_id=message.chat.id,
            text=i18n.get(
                "error-reply",
                await get_locale(
                    chat_id=message.chat.id
                )
            )
        )

    reply_user: User = message.reply_to_message.from_user
    admin_user: User = message.from_user
    chat_id: int = message.chat.id
    user_id: int = reply_user.id
    user_full_name: str = reply_user.full_name
    admin_full_name: str = admin_user.full_name
    locale: str = await get_locale(chat_id=chat_id)

    await unban_with_message(
        bot=bot,
        chat_id=chat_id,
        user_id=user_id,
        i18n=i18n,
        message_text=i18n.get(
            "unban-user",
            locale,
            user_id=user_id,
            user_full_name=user_full_name,
            admin_full_name=admin_full_name,
            admin_id=admin_user.id
        )
    )
