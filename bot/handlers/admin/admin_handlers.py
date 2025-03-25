import logging

from typing import Optional
from aiogram import Bot, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from bot.filters.admin_filters import is_admin

from bot.utils.moderation.moderate_restricts import (
    handler_to_ban, handler_to_mute, 
    handler_to_unban, handler_to_unmute
)

from bot.database.requests.sqlalchemy.users_requests import add_user
from bot.database.requests.sqlalchemy.warns_system import add_warn_with_add_user


admin_command = Router()


@admin_command.message(Command("mute"))
@is_admin
async def mute_users(message: Message, command: CommandObject) -> None:
    bot: Optional[Bot] = message.bot

    if not message.reply_to_message:
        await message.reply("reply to message users")
        return

    await handler_to_mute(bot, message)


@admin_command.message(Command("ban"))
@is_admin
async def ban_users(message: Message, command: CommandObject) -> None:
    bot: Optional[Bot] = message.bot

    if not message.reply_to_message:
        await message.reply("reply to message users")
        return

    await handler_to_ban(bot, message)


@admin_command.message(Command("unmute"))
@is_admin
async def unmute_user(message: Message, command: CommandObject) -> None:
    bot: Optional[Bot] = message.bot

    if not message.reply_to_message:
        await message.reply("reply to message users")
        return

    await handler_to_unmute(bot, message)


@admin_command.message(Command("unban"))
@is_admin
async def unmute_user(message: Message, command: CommandObject) -> None:
    bot: Optional[Bot] = message.bot

    if not message.reply_to_message:
        await message.reply("reply to message users")
        return

    await handler_to_unban(bot, message)


@admin_command.message(Command("add"))
@is_admin
async def test_add_user(message: Message, command: CommandObject) -> None:
    bot: Optional[Bot] = message.bot
    user_id: Optional[int] = message.from_user.id

    await add_user(user_id)

    await message.reply("Add to DataBase. Status: Succes")


@admin_command.message(Command("warn"))
@is_admin
async def warn_user(message: Message, command: CommandObject) -> None:
    bot: Optional[Bot] = message.bot
    user_id: Optional[int] = message.from_user.id
    user_name: Optional[str] = message.from_user.username

    if not message.reply_to_message:
        await message.reply("reply to message users")
        return
    
    
    await add_warn_with_add_user(user_id)

    await message.reply(f"User {user_name} has been warned")

    