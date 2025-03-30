import asyncio
import os

import logging

from aiogram import Bot, Dispatcher
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentRuntimeCore
from dotenv import load_dotenv

from bot.handlers.admin.admin_handlers import admin_command
from bot.handlers.empty.emty_chat_member_handlers import empty_member

from bot.middlewares import setup_middlewares

load_dotenv()


async def main() -> None:
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        raise ValueError("BOT_TOKEN")
    
    dp: Dispatcher = Dispatcher()
    bot: Bot = Bot(token=TOKEN)
    i18n_middleware: I18nMiddleware = I18nMiddleware(
        core=FluentRuntimeCore(
            path="bot/locales/{locale}",
            default_locale="en"
        ),
    )

    i18n_middleware.setup(dispatcher=dp)

    dp.include_routers(admin_command, empty_member)
    setup_middlewares(dp=dp, bot=bot)

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
