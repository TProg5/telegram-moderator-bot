import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentRuntimeCore
from dotenv import load_dotenv

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
            path="bot/locales/{locale}",
        ),
    )

    i18n_middleware.setup(dispatcher=dp)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:        
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")
