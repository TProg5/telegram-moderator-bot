from typing import List

from aiogram import Bot, Dispatcher

from .AdminMiddleware import CallbackAdminCheckerMiddleware
from .throotling_middleware import ThrottlingMiddleware

def setup_inner_middlewares(bot: Bot, dp: Dispatcher) -> None:
    dp.message.middleware(ThrottlingMiddleware(5))
    dp.callback_query.middleware(CallbackAdminCheckerMiddleware(bot=bot))


__all__: List[str] = ["setup_inner_middlewares"]