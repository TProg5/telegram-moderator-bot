import asyncio
import logging

from bot.config import TOKEN

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession

from bot.handlers.admins.admin_handlers import admin_command
from bot.Middlewares.inner.ThrottlingMiddleware import ThrottlingMiddleware
from bot.Middlewares.outer.NewMemberMiddleware import WelcomeMiddleware

dp = Dispatcher()

session = AiohttpSession()
bot = Bot(token=TOKEN, session=session)

dp.include_router(admin_command)

dp.chat_member.middleware(WelcomeMiddleware(bot=bot))
dp.message.middleware(ThrottlingMiddleware())


async def main() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:        
        print("Bot started")
        logging.basicConfig(level=logging.INFO)
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")
