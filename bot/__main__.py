import logging

import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentRuntimeCore
from dotenv import load_dotenv

from bot.middlewares import setup_middlewares
from bot.handlers import setup_routers

load_dotenv()


async def main() -> None:
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        raise ValueError("BOT_TOKEN")
    
    dp: Dispatcher = Dispatcher()
    bot: Bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(
            parse_mode="HTML"
        )
    )
    i18n_middleware: I18nMiddleware = I18nMiddleware(
        core=FluentRuntimeCore(
            path="bot/locales/{locale}"
        ),
    )

    setup_middlewares(bot=bot, dp=dp)
    setup_routers(dp=dp)
    i18n_middleware.setup(dispatcher=dp)


    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types()
    )


if __name__ == "__main__":
    try:
        print("Bot runned")
        logging.basicConfig(level=logging.INFO)    
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")
