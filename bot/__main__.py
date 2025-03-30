import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentRuntimeCore
from dotenv import load_dotenv

# from bot.middlewares import setup_middlewares
from bot.handlers import admin_command

# load_dotenv()


async def main() -> None:
    # TOKEN = os.getenv("BOT_TOKEN")
    # if not TOKEN:
    #     raise ValueError("BOT_TOKEN")
    
    dp: Dispatcher = Dispatcher()
    bot: Bot = Bot(
        token="7689440867:AAF7uOFi0F0j0UhvOQmqK1gEg6m9izQ2kaE",
        default=DefaultBotProperties(
            parse_mode="HTML"
        )
    )
    i18n_middleware: I18nMiddleware = I18nMiddleware(
        core=FluentRuntimeCore(
            path="bot/locales/{locale}"
        ),
    )

    dp.include_router(router=admin_command)
    i18n_middleware.setup(dispatcher=dp)


    # await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types()
    )


if __name__ == "__main__":
    try:        
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")
