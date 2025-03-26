import asyncio
import os

import logging

from aiogram import Bot, Dispatcher
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentRuntimeCore
from dotenv import load_dotenv

from bot.handlers.admin.admin_handlers import admin_command

# from bot.middlewares import setup_middlewares

load_dotenv()


async def main() -> None:
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        raise ValueError("BOT_TOKEN")
    
    dp: Dispatcher = Dispatcher()
    bot: Bot = Bot(token=TOKEN)
    i18n_middleware: I18nMiddleware = I18nMiddleware(
        core=FluentRuntimeCore(
            path="bot/locale",
        ),
    )

    i18n_middleware.setup(dispatcher=dp)

    dp.include_router(admin_command)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        print("Bot runned")
        logging.basicConfig(level=logging.INFO)
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")
