from typing import List

from aiogram import Bot, Dispatcher

from .goodbye_middleware import GoodbyeMiddleware
from .welcome_middleware import WelcomeMiddleware


def setup_outer_middlewares(bot: Bot, dp: Dispatcher) -> None:
    dp.chat_member.outer_middleware(GoodbyeMiddleware(bot=bot))
    dp.chat_member.outer_middleware(WelcomeMiddleware(bot=bot))


__all__: List[str] = ["setup_outer_middlewares"]