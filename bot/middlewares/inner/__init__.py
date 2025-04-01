from typing import List

from aiogram import Bot, Dispatcher

from bot.handlers.admin import admin_command
from .admin_checker import CallbackAdminCheckerMiddleware, AdminCheckerMiddleware
from .throotling_middleware import ThrottlingMiddleware

def setup_inner_middlewares(bot: Bot, dp: Dispatcher) -> None:
    dp.message.middleware(ThrottlingMiddleware(limit=5))
    admin_command.message.middleware(AdminCheckerMiddleware(bot=bot))
    admin_command.callback_query.middleware(CallbackAdminCheckerMiddleware(bot=bot))


__all__: List[str] = ["setup_inner_middlewares"]