from aiogram import Bot, Router

from aiogram.types import ChatMemberUpdated


empty_member = Router()


@empty_member.chat_member()
async def fallback_handler(event: ChatMemberUpdated):
    pass